import json
import logging

from zygoat.constants import Projects, Phases
from zygoat.components import Component
from zygoat.utils.shell import run
from zygoat.utils.files import use_dir

from .mui import mui

log = logging.getLogger()


class Dependencies(Component):
    dependencies = ["prop-types", "axios", "next-compose-plugins", "next-svgr", "next-images"]
    dev_dependencies = ["jest", "@testing-library/dom", "@testing-library/react"]

    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing frontend production dependencies")
            run(["yarn", "add", *self.dependencies])

            log.info("Installing frontend dev dependencies")
            run(["yarn", "add", "--dev", *self.dev_dependencies])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)
        with use_dir(Projects.FRONTEND):
            log.info("Upgrading frontend dependencies")
            run(["yarn", "upgrade"])

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


dependencies = Dependencies(sub_components=[mui])
