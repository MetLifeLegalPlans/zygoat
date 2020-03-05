import logging
import os
import requests

from zygoat.components import Component

log = logging.getLogger()

file_name = ".gitignore"


class GitIgnore(Component):
    def create(self):
        with open(file_name, "a") as f:
            log.info("Retrieving node gitignore info")
            res = requests.get("https://gitignore.io/api/node")
            res.raise_for_status()

            f.write(res.text + "\n")
            f.write(".tern-port")

    @property
    def installed(self):
        if not os.path.exists(file_name):
            return False

        with open(file_name) as f:
            return "api/node" in f.read()


gitignore = GitIgnore()
