import logging

from zygoat.components import Component
from zygoat.constants import Phases, Projects, Images
from zygoat.utils.shell import multi_docker_run

log = logging.getLogger()


class Reformat(Component):
    def create(self):
        multi_docker_run(
            [["pip", "install", "black"], ["black", "."]],
            self.docker_image(Images.PYTHON),
            Projects.BACKEND,
        )

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        return False  # Always run this, no matter what


reformat = Reformat()
