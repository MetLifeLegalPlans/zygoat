import json
import logging

from zygoat.constants import Projects, Phases, Images
from zygoat.components import Component
from zygoat.utils.shell import docker_run
from zygoat.utils.files import use_dir

from .eslintrc import eslintrc

log = logging.getLogger()


class Eslint(Component):
    dependencies = [
        "eslint",
    ]

    plugins = [
        f"eslint-plugin-{name}"
        for name in ["import", "jest", "jsx-a11y", "prettier", "react", "react-hooks"]
    ]

    configs = [f"eslint-config-{name}" for name in ["airbnb", "prettier"]]

    def create(self):
        log.info("Installing eslint dev dependencies to frontend")
        docker_run(
            ["yarn", "add", "--dev", *self.dependencies],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        log.info("Installing eslint plugins to frontend")
        docker_run(
            ["yarn", "add", "--dev", *self.plugins],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        log.info("Installing eslint configs to frontend")
        docker_run(
            ["yarn", "add", "--dev", *self.configs],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        with use_dir(Projects.FRONTEND):
            log.info("Adding eslint command")
            with open("package.json") as f:
                data = json.load(f)
                data["scripts"]["lint"] = "eslint --ext .js,.jsx ."
                data["scripts"]["fix"] = "yarn lint --fix"

            log.info("Dumping new frontend package file")
            with open("package.json", "w") as f:
                json.dump(data, f)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                current = list(json.load(f).get("devDependencies", {}).keys())
                return all(
                    package in current
                    for package in self.dependencies + self.plugins + self.configs
                )


eslint = Eslint(sub_components=[eslintrc])
