from importlib import resources as il_resources
import logging
import os

from zygoat.components import Component
from zygoat.constants import Projects, Phases
from zygoat.utils.files import use_dir

from .docker_compose import docker_compose
from . import resources

log = logging.getLogger()
file_name = "Dockerfile"


class Dockerfile(Component):
    def create(self):
        with use_dir(Projects.FRONTEND):
            with open(file_name, "w") as f:
                log.info("Writing frontend Dockerfile")
                f.write(il_resources.read_text(resources, file_name))

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        return os.path.exists(os.path.join(Projects.FRONTEND, file_name))


dockerfile = Dockerfile(sub_components=[docker_compose])
