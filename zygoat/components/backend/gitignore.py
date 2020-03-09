import logging
import os
import requests

from zygoat.components import Component

log = logging.getLogger()

file_name = ".gitignore"


class GitIgnore(Component):
    def create(self):
        with open(file_name, "a") as f:
            log.info("Retrieving python gitignore info")
            res = requests.get("https://gitignore.io/api/python")
            res.raise_for_status()

            f.write(res.text)
            f.write("\n# IntelliJ editors\n.idea/")
            # End with a newline since js-specific stuff will go into the
            # file next.
            f.write("\n\n# Swap files\n*.swp\n")
            f.write("\n\n# Virtual Environments\nvenv/")

    @property
    def installed(self):
        if not os.path.exists(file_name):
            return False

        with open(file_name) as f:
            return "api/python" in f.read()


gitignore = GitIgnore()
