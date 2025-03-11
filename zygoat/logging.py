from colorama import Fore, Style, init
import logging

init()

color_mappings = {
    logging.DEBUG: Fore.WHITE,
    logging.INFO: Fore.CYAN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED,
}


class Formatter(logging.Formatter):
    def format(self, record):
        return " ".join(
            [
                Style.BRIGHT + color_mappings[record.levelno] + record.levelname,
                Fore.RESET + "=>" + Style.RESET_ALL,
                record.msg,
            ]
        )


log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(Formatter(""))
ch.setLevel(logging.INFO)
log.addHandler(ch)
