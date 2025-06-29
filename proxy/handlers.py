from PyRoxy import Proxy, ProxyChecker, ProxyUtiles
from random import choice as randchoice
from typing import Set

from config.environment import logger
from core.tools import bcolors
from proxy.proxy_manager import ProxyManager


def handleProxyList(threads, con, proxy_li, proxy_ty, url=None):
    if proxy_ty not in {4, 5, 1, 0, 6}:
        exit("Socks Type Not Found [4, 5, 1, 0, 6]")
    if proxy_ty == 6:
        proxy_ty = randchoice([4, 5, 1])
    if not proxy_li.exists():
        logger.warning(
            f"{bcolors.WARNING}The file doesn't exist, creating files and downloading proxies.{bcolors.RESET}")
        proxy_li.parent.mkdir(parents=True, exist_ok=True)
        with proxy_li.open("w") as wr:
            Proxies: Set[Proxy] = ProxyManager.DownloadFromConfig(con, proxy_ty)
            logger.info(
                f"{bcolors.OKBLUE}{len(Proxies):,}{bcolors.WARNING} Proxies are getting checked, this may take awhile{bcolors.RESET}!"
            )
            Proxies = ProxyChecker.checkAll(
                Proxies, timeout=5, threads=threads,
                url=url.human_repr() if url else "http://httpbin.org/get",
            )

            if not Proxies:
                exit(
                    "Proxy Check failed, Your network may be the problem"
                    " | The target may not be available."
                )
            stringBuilder = ""
            for proxy in Proxies:
                stringBuilder += (proxy.__str__() + "\n")
            wr.write(stringBuilder)

    proxies = ProxyUtiles.readFromFile(proxy_li)
    if proxies:
        logger.info(f"{bcolors.WARNING}Proxy Count: {bcolors.OKBLUE}{len(proxies):,}{bcolors.RESET}")
    else:
        logger.info(
            f"{bcolors.WARNING}Empty Proxy File, running flood without proxy{bcolors.RESET}")
        proxies = None

    return proxies
