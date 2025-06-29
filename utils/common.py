from logging import shutdown
from os import _exit
from config.environment import logger
from core.tools import bcolors

def exit(*message):
    if message:
        logger.error(bcolors.FAIL + " ".join(message) + bcolors.RESET)
    shutdown()
    _exit(1)