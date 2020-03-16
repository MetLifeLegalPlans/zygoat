import logging
import os

from zygoat.components import Component
from zygoat.constants import Phases, Projects, VENV
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

log = logging.getLogger()


class Reformat(Component):
    def create(self):
        with use_dir(Projects.BACKEND):
            black = os.path.join(VENV, "bin", "black")
            if os.path.exists(black):
                run([black, ".", "--exclude", VENV])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


reformat = Reformat()
