import json
import logging

from zygoat.components import Component
from zygoat.constants import Projects, Phases
from zygoat.utils.shell import run
from zygoat.utils.files import use_dir

log = logging.getLogger()


class BePretty(Component):
    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing be-pretty into frontend project")
            run(["yarn", "add", "--dev", "be-pretty"])

            log.info("Configuring be-pretty to use the correct RC file")
            run(["yarn", "run", "be-pretty", "setDefault"])

            log.info("Formatting project with prettier")
            run(["yarn", "run", "be-pretty", "formatAll"])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                return "be-pretty" in json.load(f).get("devDependencies", {})


be_pretty = BePretty()
