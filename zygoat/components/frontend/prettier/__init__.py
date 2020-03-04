import json
import logging

from zygoat.components import Component
from zygoat.constants import Projects, Phases
from zygoat.utils.shell import run
from zygoat.utils.files import use_dir

from .prettierrc import prettierrc
from .be_pretty import be_pretty
from .pretty_quick import pretty_quick

log = logging.getLogger()


class Prettier(Component):
    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing prettier dev dependency into the frontend project")
            run(["yarn", "add", "--dev", "prettier"])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                return "prettier" in json.load(f).get("devDependencies", {})


prettier = Prettier(sub_components=[prettierrc, be_pretty, pretty_quick])
