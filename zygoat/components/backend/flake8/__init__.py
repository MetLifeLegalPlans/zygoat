import logging

from zygoat.components import Component
from zygoat.constants import Phases
from zygoat.utils.backend import install_dependencies


from .configuration import configuration

log = logging.getLogger()


class Flake8(Component):
    def create(self):
        dependencies = [
            "flake8",
            "flake8-mock",
            "flake8-commas",
            "flake8-quotes",
            "flake8-debugger",
            "flake8-builtins",
            "flake8-deprecated",
            "flake8-comprehensions",
        ]

        log.info("Installing flake8 dev dependencies")
        install_dependencies(*dependencies, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


flake8 = Flake8(sub_components=[configuration])
