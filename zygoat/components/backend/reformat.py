import logging
from shutil import which

from zygoat.components import Component
from zygoat.constants import Phases, Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

log = logging.getLogger()


class Reformat(Component):
    def create(self):
        with use_dir(Projects.BACKEND):
            black = which("black")
            if black is not None:
                run([black, "."])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


reformat = Reformat()
