from colorama import Fore, Style, init
import logging

init()

color_mappings = {
    'DEBUG': Fore.WHITE,
    'INFO': Fore.CYAN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.RED,
}


class Formatter(logging.Formatter):
    def format(self, record):
        return ' '.join([
            Style.BRIGHT + color_mappings[record.levelname] + record.levelname,
            Fore.RESET + '=>' + Style.RESET_ALL,
            record.msg,
        ])


log = logging.getLogger()
ch = logging.StreamHandler()
ch.setFormatter(Formatter(''))
log.addHandler(ch)
