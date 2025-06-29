from logging import basicConfig, getLogger
from ssl import create_default_context, CERT_NONE
from certifi import where
from socket import socket, AF_INET, SOCK_DGRAM
from pathlib import Path
from json import load

basicConfig(format='[%(asctime)s - %(levelname)s] %(message)s', datefmt="%H:%M:%S")
logger = getLogger("MHDDoS")
logger.setLevel("INFO")

ctx = create_default_context(cafile=where())
ctx.check_hostname = False
ctx.verify_mode = CERT_NONE

__version__ = "2.4 SNAPSHOT"
__dir__ = Path(__file__).parent.parent
__ip__ = None

with socket(AF_INET, SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    __ip__ = s.getsockname()[0]

with open(__dir__ / "config.json") as f:
    con = load(f)
