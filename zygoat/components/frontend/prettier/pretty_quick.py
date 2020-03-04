import json
import logging

from zygoat.components import Component
from zygoat.constants import Projects, Phases
from zygoat.utils.shell import run
from zygoat.utils.files import use_dir

log = logging.getLogger()


class PrettyQuick(Component):
    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing pretty-quick into frontend project")
            run(["yarn", "add", "--dev", "pretty-quick"])

            log.info("Adding pretty-quick lint command")
            with open("package.json") as f:
                data = json.load(f)
                data["scripts"]["pretty-lint"] = "pretty-quick --check --branch"

            log.info("Dumping new frontend package file")
            with open("package.json", "w") as f:
                json.dump(data, f)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        with use_dir(Projects.FRONTEND):
            with open("package.json") as f:
                data = json.load(f)

                return (
                    "pretty-quick" in data.get("devDependencies", {})
                    and "pretty-lint" in data["scripts"]
                )


pretty_quick = PrettyQuick()
