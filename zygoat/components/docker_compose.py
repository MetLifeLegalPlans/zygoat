import logging
import os

from . import Component
from . import resources

from importlib import resources as il_resources

log = logging.getLogger()
file_name = "docker-compose.yml"


class DockerCompose(Component):
    def create(self):
        log.info("Creating an empty docker-compose.yml file")

        # All phases and checks run from the repository root
        with open(file_name, "w") as f:
            f.write(il_resources.read_text(resources, file_name))

        log.info(f"Created {file_name} successfully")

    def delete(self):
        log.warning(f"Deleting {file_name}")
        os.remove(file_name)

    @property
    def installed(self):
        return os.path.exists(file_name)


docker_compose = DockerCompose()
