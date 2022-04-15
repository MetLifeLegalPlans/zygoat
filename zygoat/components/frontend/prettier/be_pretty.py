import json
import logging

from zygoat.components import Component
from zygoat.constants import Projects, Phases, Images
from zygoat.utils.shell import docker_run
from zygoat.utils.files import use_dir

log = logging.getLogger()


class BePretty(Component):
    def create(self):
        log.info("Installing be-pretty into frontend project")
        docker_run(
            ["yarn", "add", "--dev", "be-pretty@0.9.5"],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        log.info("Configuring be-pretty to use the correct RC file")
        docker_run(
            ["yarn", "run", "be-pretty", "setDefault"],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        log.info("Formatting project with prettier")
        docker_run(
            ["yarn", "run", "be-pretty", "formatAll"],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                return "be-pretty" in json.load(f).get("devDependencies", {})


be_pretty = BePretty()
