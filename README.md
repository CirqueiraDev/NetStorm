<h1 align="center">NetStorm - DDoS Attack Script With 55 Methods</h1>
<em><h5 align="center">(Programming Language - Python 3)</h5></em>

<p align="center">
<a href="#"><img alt="NetStorm last commit (main)" src="https://img.shields.io/github/last-commit/CirqueiraDev/NetStorm/main?color=green&style=for-the-badge"></a>
<a href="#"><img alt="NetStorm" src="https://img.shields.io/badge/version-1.0-blueviolet?style=for-the-badge&logo=github"></a>
<a href="#"><img alt="NetStorm" src="https://img.shields.io/badge/status-dev-blue?style=for-the-badge&logo=python"></a>

<p align="center">Please don't attack websites without the owner's consent.</p>

<p align="center"><img src="https://github.com/user-attachments/assets/5ff90473-73ac-4489-a38e-9682f375dce3" width="950" height="450" alt="SCRIPT"></p>


---

## Features And Methods

### 💣 Layer 7 Methods

|               | Comando    | Descrição                                                           |
|---------------|------------|----------------------------------------------------------------------|
| `get`         | GET        | GET Flood                                                           |
| `post`        | POST       | POST Flood                                                          |
| `ovh`         | OVH        | Bypass OVH                                                         |
| `ovh`         | RHEX       | Random HEX                                                         |
| `ovh`         | STOMP      | Bypass chk_captcha                                                 |
| `stress`      | STRESS     | Send HTTP Packet With High Byte                                    |
| `dyn`         | DYN        | Method with Random SubDomain                                       |
| `downloader`  | DOWNLOADER | Read data slowly                                                   |
| `slow`        | SLOW       | Slowloris (classic method)                                         |
| `head`        | HEAD       | [HTTP HEAD](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD) |
| `null`        | NULL       | Null User-Agent and other headers                                  |
| `cookie`      | COOKIE     | Random Cookie (`isset($_COOKIE)`)                                 |
| `pps`         | PPS        | Only `GET / HTTP/1.1\r\n\r\n`                                      |
| `even`        | EVEN       | GET with extended headers                                          |
| `googleshield`| GSB        | Google Project Shield Bypass                                       |
| `ddosguard`   | DGB        | DDoS Guard Bypass                                                  |
| `arvancloud`  | AVB        | Arvan Cloud Bypass                                                 |
| `bot`         | BOT        | Imitate Google bot                                                 |
| `apache`      | APACHE     | Apache Exploit                                                     |
| `xmlrpc`      | XMLRPC     | WP XMLRPC exploit (`/xmlrpc.php`)                                 |
| `cfb`         | CFB        | CloudFlare Bypass                                                  |
| `bypass`      | BYPASS     | Generic AntiDDoS Bypass                                            |
| `tor`         |  TOR      | Bypass Onion websites                                              |

---

### 🧨 Layer 4 Methods

|               | Comando      | Descrição                                               |
|---------------|--------------|----------------------------------------------------------|
| `tcp`         | TCP          | TCP Flood Bypass                                        |
| `udp`         | UDP          | UDP Flood Bypass                                        |
| `syn`         | SYN          | SYN Flood                                               |
| `ovh`         | OVH-UDP      | UDP with random headers/payload to bypass OVH/WAF       |
| `cps`         | CPS          | Open and close connections with proxy                   |
| `icmp`        | ICMP         | ICMP Echo Request Flood (Layer3)                        |
| `connection`  | CONNECTION   | Keep connections alive with proxy                       |
| `vse`         | VSE          | Valve Source Engine Protocol                            |
| `ts3`         | TS3          | TeamSpeak 3 Status Ping                                 |
| `fivem`       | FIVEM        | FiveM Status Ping                                       |
| `fivem-token` | FIVEM-TOKEN  | FiveM Token Flood                                       |
| `discord`     | DISCORD      | Custom RAW packet flood                                 |
| `mem`         | MEM          | Memcached Amplification                                 |
| `ntp`         | NTP          | NTP Amplification                                       |
| `mcbot`       | MCBOT        | Minecraft Bot Flood                                     |
| `minecraft`   | MINECRAFT    | Minecraft Status Ping                                   |
| `mcpe`        | MCPE         | Minecraft PE Status Ping                                |
| `dns`         | DNS          | DNS Amplification                                       |
| `char`        | CHAR         | Chargen Amplification                                   |
| `cldap`       | CLDAP        | CLDAP Amplification                                     |
| `ard`         | ARD          | Apple Remote Desktop Amplification                      |
| `rdp`         | RDP          | Remote Desktop Protocol Amplification                   |

---

### ⚙️ Tools

> Run with: `python3 start.py tools`

| Command    | Description                                                |
|------------|------------------------------------------------------------|
| `cfip`     | Find the real IP behind Cloudflare                         |
| `dns`      | Show DNS records                                           |
| `tssrv`    | Resolve TeamSpeak SRV records                              |
| `ping`     | Send ping packets                                          |
| `check`    | Check the status of a website                              |
| `dstat`    | Show traffic (bytes received and sent)                     |

| Command    | Description                     |
|------------|----------------------------------|
| `stop`     | Stop all running attacks         |
| `tools`    | Open tools menu                  |
| `help`     | Show usage instructions          |

---

### ⚠️ Legal Disclaimer

This project is intended for authorized testing and educational purposes only. Misuse may violate local and international laws. You are solely responsible for how you use this tool.

---

### 🚀 Installation

```bash
git clone https://github.com/CirqueiraDev/NetStorm.git
cd NetStorm
pip install -r requirements.txt
```

---

### Créditos

- Original script developed by [**MatrixTM**](https://github.com/MatrixTM/MHDDoS)

- Modified and maintained by [**CirqueiraDev**](https://github.com/CirqueiraDev)


### Redes Sociais
- For more information, contact me: [Telegram](https://t.me/cirqueiraz)
- **Discord: Cirqueira**
- <a href="https://www.instagram.com/cirqueirax/">Instagram</a>
