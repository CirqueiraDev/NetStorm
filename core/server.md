Description
-----------
This module implements a CNC (Command-and-Control) server that enables
remote control of NetStorm via an authenticated TCP connection. The server
performs an authentication handshake (key) and receives **JSON commands**
to list, search and stop tasks, and also accepts method-style commands
(parameters depend on the method). Responses are also JSON in the standard
format described below.

Main behavior
-------------
- Opens a TCP socket and waits for connections.
- Performs an authentication handshake using the configured key (con['KEY']).
- After authentication, accepts JSON commands and returns JSON responses in
  the standard format: {"status": "...", "message": "...", "data": {...}}.
- Keeps an in-memory registry (`self.attacks`) of running tasks/threads and
  provides operations to list, search and stop tasks.

JSON commands (overview)
------------------------
The server processes JSON containing a main command followed by required fields.
Examples and templates below are **sanitized/safe** and only demonstrate structure:

Administrative commands (safe)
- LIST
  - Returns a list of running tasks.
  - Example:
```json
{
  "command": "LIST"
}
```

* SEARCH

  * Retrieves task details by `attack_id` or `sign`.
  * Example:

```json
{
  "command": "SEARCH",
  "attack_id": "uuid-here"
}
```

* STOP

  * Stops a task identified by `attack_id` or `sign`.
  * Example:

```json
{
  "command": "STOP",
  "attack_id": "uuid-here"
}
```

Safe template for methods (FORMAT ONLY — not an example of harmful use)

* General structure used by the server for method-based tasks:

* Layer 7
```json
{
  "method": "<METHOD_NAME>",
  "target": "<host-or-url>",
  "socks_type": <0|1|...>,
  "threads": <number>,
  "proxylist": "<proxies_file.txt>",
  "rpc": <number>,
  "duration": <seconds>,
  "attack_id": "<uuid-here>",
  "sign": "<any-identifier>"
}
```

* Layer 4
```json
{
    "method": "UDP",
    "target": "IP:PORT",
    "threads": <number>,
    "duration": <seconds>,
    "attack_id": "<uuid-here>",
    "sign": "<any-identifier>"
}
```

* Layer 4 with proxy
```json
{
    "method": "MCBOT",
    "target": "IP:PORT",
    "threads": <number>,
    "duration": <seconds>,
    "socks_type": <number>,
    "proxylist": "<file.txt>",
    "attack_id": "<uuid-here>",
    "sign": "<any-identifier>"
}
```

* Layer 4 Amplification
```json
{
    "method": "CLDAP",
    "target": "IP:PORT",
    "threads": <number>,
    "duration": <seconds>,
    "reflector_file": "<reflector_file.txt>",
    "attack_id": "u<uid-here>",
    "sign": "<any-identifier>"
}
```

Note: the above is **only a field template** for server parsing/validation.
DO NOT perform load tests or any operation that may impact third parties
without explicit authorization from the resource owner.

## JSON response format

All responses follow this structure:

```json
{
  "status": "success" | "error" | "failed",
  "message": "<short message>",
  "data": { ... }    # optional, with extra data
}
```

## Security and best practices

* **Authentication**: the key in `con['KEY']` is required — keep it strong and secret.
* **Network**: protect the server with a firewall; allow only authorized IPs when possible.
* **Logging/monitoring**: log connections and relevant events; avoid sensitive data in logs.
* **Legality**: load/stress testing must be performed only on systems for which you
  have explicit permission. Misuse can be illegal.

## Implementation notes

* The server stores entries in `self.attacks` keyed by `sign` (or other associated key).
  Each entry contains: thread, event and info (attack_id, method, target, ...).
* To stop tasks, the server attempts to clear the associated `Event` and to stop/join
  the thread when possible.
* DNS resolution, file checks (useragents, referers, proxies) and parameter validation
  are performed before starting a task.
