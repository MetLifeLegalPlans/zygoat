import sys
import logging

from .config import Config

log = logging.getLogger()


class Project:
    def __init__(self):
        try:
            self.config = Config()
        except FileNotFoundError as e:
            log.critical(e)
            sys.exit(1)

    def create(self):
        pass
