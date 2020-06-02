import importlib
import logging

from zygoat.constants import Projects
from zygoat.components import Component
from zygoat.config import yaml
from . import resources

log = logging.getLogger()
file_name = "docker-compose.yml"


class DockerCompose(Component):
    def _dump_config(self, data):
        with open(file_name, "w") as root_config:
            yaml.dump(data, root_config)

    def _load_config(self):
        with open(file_name) as root_config:
            return yaml.load(root_config.read())

    def create(self):
        log.info(f"Reading {file_name} from the repo")

        config = self._load_config()
        config["services"].update(
            yaml.load(importlib.resources.read_text(resources, file_name))
        )

        log.info("Dumping updated docker-compose config")
        self._dump_config(config)

    def delete(self):
        config = self._load_config()

        log.info("Removing backend and DB services from config")
        del config["services"][Projects.BACKEND]
        del config["services"]["db"]

        log.info("Dumping updated docker-compose config")
        self._dump_config(config)

    @property
    def installed(self):
        services = self._load_config()["services"]

        return Projects.BACKEND in services and "db" in services


docker_compose = DockerCompose()
