import json
import logging

from zygoat.constants import Projects, Phases, Images
from zygoat.components import Component
from zygoat.utils.shell import docker_run
from zygoat.utils.files import use_dir

from .mui import mui
from .jest_config import jest_config
from .jest_setup import jest_setup

log = logging.getLogger()


class Dependencies(Component):
    dependencies = [
        "prop-types",
        "axios",
        "next-compose-plugins",
        "next-svgr",
        "next-images",
        "window-or-global",
    ]
    dev_dependencies = [
        "jest",
        "react-axe",
        "@testing-library/dom",
        "@testing-library/react",
        "@testing-library/jest-dom",
        "css-mediaquery",
    ]

    def create(self):
        log.info("Installing frontend production dependencies")
        docker_run(
            ["yarn", "add", *self.dependencies],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        log.info("Installing frontend dev dependencies")
        docker_run(
            ["yarn", "add", "--dev", *self.dev_dependencies],
            self.docker_image(Images.NODE),
            Projects.FRONTEND,
        )

        with use_dir(Projects.FRONTEND):
            log.info("Adding jest test commands")
            with open("package.json") as f:
                data = json.load(f)
                data["scripts"]["test"] = "jest"
                data["scripts"]["test-coverage"] = "jest --coverage"

            log.info("Dumping new frontend package file")
            with open("package.json", "w") as f:
                json.dump(data, f)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)
        log.info("Upgrading frontend dependencies")
        docker_run(["yarn", "upgrade"], self.docker_image(Images.NODE), Projects.FRONTEND)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                data = json.load(f)

                def check(dependency_name, path):
                    return dependency_name in data[path]

                for dep_set, path_key in [
                    [self.dependencies, "dependencies"],
                    [self.dev_dependencies, "devDependencies"],
                ]:
                    for dep in dep_set:
                        if not check(dep, path_key):
                            return False

                return True


dependencies = Dependencies(sub_components=[mui, jest_config, jest_setup])
