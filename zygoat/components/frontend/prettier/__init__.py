import json
import logging

from zygoat.components import Component
from zygoat.constants import Projects, Phases
from zygoat.utils.shell import docker_run
from zygoat.utils.files import use_dir

from .prettierrc import prettierrc
from .be_pretty import be_pretty
from .pretty_quick import pretty_quick
from .prettierignore import prettierignore

log = logging.getLogger()


class Prettier(Component):
    def create(self):
        log.info("Installing prettier dev dependency into the frontend project")
        docker_run(
            ["yarn", "add", "--dev", "prettier"], self.docker_image("NODE"), Projects.FRONTEND
        )

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                return "prettier" in json.load(f).get("devDependencies", {})


prettier = Prettier(sub_components=[prettierrc, be_pretty, pretty_quick, prettierignore])
