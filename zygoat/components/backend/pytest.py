import logging

from zygoat.components import FileComponent, Component
from zygoat.constants import Projects, Phases
from zygoat.utils.backend import install_dependencies

from . import resources

log = logging.getLogger()


class PytestConfig(FileComponent):
    filename = "pytest.ini"
    resource_pkg = resources
    base_path = Projects.BACKEND


class Pytest(Component):
    def create(self):
        dependencies = [
            "pytest",
            "pytest-django",
            "pytest-cov",
        ]

        log.info("Installing pytest dev dependencies")
        install_dependencies(*dependencies, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


pytest = Pytest(sub_components=[PytestConfig()])
