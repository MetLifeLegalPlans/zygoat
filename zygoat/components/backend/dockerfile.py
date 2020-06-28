import importlib
import logging
import os

from zygoat.components import Component
from . import resources

from zygoat.utils.files import use_dir
from zygoat.constants import Projects

from .docker_compose import docker_compose

log = logging.getLogger()
file_name = "Dockerfile.local"


class Dockerfile(Component):
    def create(self):
        with use_dir(Projects.BACKEND):
            log.info(f"Installing Local Dockerfile for project {Projects.BACKEND}")
            with open(file_name, "w") as f:
                f.write(importlib.resources.read_text(resources, file_name))

    def delete(self):
        with use_dir(Projects.BACKEND):
            log.info(f"Deleting {file_name}")
            os.remove(file_name)

    @property
    def installed(self):
        return os.path.exists(os.path.join(Projects.BACKEND, file_name))


dockerfile = Dockerfile(sub_components=[docker_compose])
