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

| Comando    | Description                                                        |
|------------|--------------------------------------------------------------------|
| GET        | GET Flood                                                          |
| POST       | POST Flood                                                         |
| OVH        | Bypass OVH                                                         |
| RHEX       | Random HEX                                                         |
| STOMP      | Bypass chk_captcha                                                 |
| STRESS     | Send HTTP Packet With High Byte                                    |
| DYN        | Method with Random SubDomain                                       |
| DOWNLOADER | Read data slowly                                                   |
| SLOW       | Slowloris (classic method)                                         |
| HEAD       | [HTTP HEAD](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD) |
| NULL       | Null User-Agent and other headers                                  |
| COOKIE     | Random Cookie (`isset($_COOKIE)`)                                  |
| PPS        | Only `GET / HTTP/1.1\r\n\r\n`                                      |
| EVEN       | GET with extended headers                                          |
| GSB        | Google Project Shield Bypass                                       |
| DGB        | DDoS Guard Bypass                                                  |
| AVB        | Arvan Cloud Bypass                                                 |
| BOT        | Imitate Google bot                                                 |
| APACHE     | Apache Exploit                                                     |
| XMLRPC     | WP XMLRPC exploit (`/xmlrpc.php`)                                  |
| CFB        | CloudFlare Bypass                                                  |
| BYPASS     | Generic AntiDDoS Bypass                                            |
|  TOR      | Bypass Onion websites                                               |

---

### 🧨 Layer 4 Methods

| Comando      | Description                                              |
|--------------|----------------------------------------------------------|
| TCP          | TCP Flood Bypass                                         |
| UDP          | UDP Flood Bypass                                         |
| SYN          | SYN Flood                                                |
| OVH-UDP      | UDP with random headers/payload to bypass OVH/WAF        |
| CPS          | Open and close connections with proxy                    |
| ICMP         | ICMP Echo Request Flood (Layer3)                         |
| CONNECTION   | Keep connections alive with proxy                        |
| VSE          | Valve Source Engine Protocol                             |
| TS3          | TeamSpeak 3 Status Ping                                  |
| FIVEM        | FiveM Status Ping                                        |
| FIVEM-TOKEN  | FiveM Token Flood                                        |
| DISCORD      | Magic Bytes UDP Flood                                    |
| MEM          | Memcached Amplification                                  |
| NTP          | NTP Amplification                                        |
| MCBOT        | Minecraft Bot Flood                                      |
| MINECRAFT    | Minecraft Status Ping                                    |
| MCPE         | Minecraft PE Status Ping                                 |
| DNS          | DNS Amplification                                        |
| CHAR         | Chargen Amplification                                    |
| CLDAP        | CLDAP Amplification                                      |
| ARD          | Apple Remote Desktop Amplification                       |
| RDP          | Remote Desktop Protocol Amplification                    |

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

### Credits:

- Original script developed by [**MatrixTM**](https://github.com/MatrixTM/MHDDoS)

- Modified and maintained by [**CirqueiraDev**](https://github.com/CirqueiraDev)


### Help:
- For more information, contact me: [Telegram](https://t.me/cirqueiraz)
- **Discord: Cirqueira**
- <a href="https://www.instagram.com/cirqueirax/">Instagram</a>
