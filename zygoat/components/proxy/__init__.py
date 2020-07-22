import importlib
import logging

from zygoat.components import Component, FileComponent
from zygoat.config import yaml

from . import resources

log = logging.getLogger()
project_key = "reverse-proxy"
compose_file_name = "docker-compose.yml"


class ReverseProxy(Component):
    pass


class Caddyfile(FileComponent):
    filename = "Caddyfile"
    resource_pkg = resources


class DockerCompose(Component):
    def _dump_config(self, data):
        with open(compose_file_name, "w") as root_config:
            yaml.dump(data, root_config)

    def _load_config(self):
        with open(compose_file_name) as root_config:
            return yaml.load(root_config.read())

    def create(self):
        log.info(f"Reading {compose_file_name} from the repo")

        config = self._load_config()
        config["services"].update(
            yaml.load(importlib.resources.read_text(resources, compose_file_name))
        )

        log.info("Dumping updated docker-compose config")
        self._dump_config(config)

    def delete(self):
        config = self._load_config()

        log.info("Removing proxy service from config")
        del config["services"][project_key]

        log.info("Dumping updated docker-compose config")
        self._dump_config(config)

    @property
    def installed(self):
        services = self._load_config()["services"]

        return project_key in services


reverse_proxy = ReverseProxy(sub_components=[Caddyfile(), DockerCompose()])
