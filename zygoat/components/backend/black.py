import logging
import os
import toml

from zygoat.constants import Projects
from zygoat.components import Component

log = logging.getLogger()
file_name = "pyproject.toml"


class Black(Component):
    def create(self):
        log.info("Adding black configuration to pyproject.toml")
        backend_file = os.path.join(Projects.BACKEND, file_name)

        with open(backend_file) as f:
            data = toml.load(f)

        data["tool"]["black"] = {"line-length": 95, "target-version": ["py39"]}
        with open(backend_file, "w") as f:
            toml.dump(data, f)


black = Black()
