Claro! Aqui está um exemplo de `README.md` para o seu projeto **NetStorm**, baseado nas informações que você passou:

````markdown
# NetStorm

NetStorm é uma ferramenta de stress test (teste de carga) para redes e aplicações, que suporta múltiplos métodos de ataque em camadas Layer4 e Layer7, com configuração flexível de proxies.

---

## Recursos

- Suporte a **55 métodos** de ataque
- Configuração automática de proxies: baixa e verifica listas de proxies se não fornecidas
- Suporte para diferentes tipos de proxy: HTTP, SOCKS4, SOCKS5, RANDOM ou todos
- Métodos para Layer4, Layer7, além de ferramentas auxiliares
- Exemplo de uso com threads e duração configuráveis

---

## Proxy Configuration

- Se a lista de proxies estiver vazia, o ataque roda sem proxy
- Se o arquivo de proxy estiver faltando, o script baixa e verifica automaticamente os proxies disponíveis

### Proxy Types

| Código | Tipo de Proxy |
|--------|--------------|
| 0      | Todos (ALL)  |
| 1      | HTTP         |
| 4      | SOCKS4       |
| 5      | SOCKS5       |
| 6      | Aleatório (RANDOM) |

---

## Métodos Suportados

### Layer4 (22 métodos)

CLDAP, ARD, FIVEM-TOKEN, ICMP, MCPE, RDP, TS3, MEM, UDP, OVH-UDP, SYN, CONNECTION, NTP, TCP, CHAR, DNS, VSE, MCBOT, FIVEM, MINECRAFT, DISCORD, CPS

### Layer7 (23 métodos)

STRESS, GSB, CFB, BOT, COOKIE, PPS, SLOW, GET, DGB, DYN, DOWNLOADER, NULL, STOMP, AVB, HEAD, EVEN, TOR, RHEX, OVH, XMLRPC, POST, BYPASS, APACHE

### Tools (7)

CFIP, DNS, TSSRV, INFO, CHECK, DSTAT, PING

### Outros (3)

TOOLS, HELP, STOP

---

## Exemplos de Uso

### Layer7

```bash
python3 main.py <method> <url> <socks_type> <threads> <proxylist> <rpc> <duration> [debug]
````

### Layer4

```bash
python3 main.py <method> <ip:port> <threads> <duration>
```

### Layer4 com Proxy

```bash
python3 main.py <method> <ip:port> <threads> <duration> <socks_type> <proxylist>
```

### Layer4 Amplification

```bash
python3 main.py <method> <ip:port> <threads> <duration> <reflector_file>
```

---

## Aviso Legal

Este projeto é destinado para testes autorizados e estudos de segurança. O uso para ataques não autorizados é ilegal e pode acarretar consequências legais.

---

## Contato

Para dúvidas ou contribuições, entre em contato.

---

**NetStorm** © 2025

```

Quer que eu gere o arquivo `.md` para você e te envie pronto?
```
