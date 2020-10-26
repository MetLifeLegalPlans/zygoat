import importlib
import logging

from zygoat.constants import Projects
from zygoat.components import Component
from zygoat.config import yaml
from . import resources

log = logging.getLogger()
file_name = "docker-compose.yml"
source_file_name = "docker-compose.cache.yml"


class Cache(Component):
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
            yaml.load(importlib.resources.read_text(resources, source_file_name))
        )

        log.info(f"Adding {Projects.CACHE} to backend dependencies")
        config["services"][Projects.BACKEND]["depends_on"].append(Projects.CACHE)

        log.info("Dumping updated docker-compose config")
        self._dump_config(config)

    def delete(self):
        config = self._load_config()

        log.info("Removing cache service from config")
        del config["services"][Projects.CACHE]

        backend_depends = config["services"][Projects.BACKEND].get("depends_on", [])

        if Projects.CACHE in backend_depends:
            backend_depends.remove(Projects.CACHE)

        config["services"][Projects.BACKEND]["depends_on"] = backend_depends

        log.info("Dumping updated docker-compose config")
        self._dump_config(config)

    @property
    def installed(self):
        services = self._load_config()["services"]

        return (
            Projects.CACHE in services
            and Projects.CACHE in services[Projects.BACKEND]["depends_on"]
        )


cache = Cache()
