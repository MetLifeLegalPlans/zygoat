from importlib import resources as il_resources
import logging
import os

from zygoat.constants import Projects, Phases
from zygoat.components import Component
from zygoat.utils.files import use_dir

from . import resources

log = logging.getLogger()

init_file = "__init__.py"
file_name = "wait_for_db.py"


# TODO: Refactor this later to avoid repetition in paths
class WaitCommand(Component):
    def _touch(self, path):
        if os.path.exists(path):
            return

        log.info(f"Creating {path}")
        open(path, "w").close()

    def create(self):
        with use_dir(Projects.BACKEND):
            log.info("Creating directory structure")
            os.makedirs(
                os.path.join(Projects.BACKEND, "management", "commands"), exist_ok=True
            )

            self._touch(os.path.join(Projects.BACKEND, "management", init_file))
            self._touch(os.path.join(Projects.BACKEND, "management", "commands", init_file))

            log.info("Copying command into project")
            with open(
                os.path.join(Projects.BACKEND, "management", "commands", file_name), "w"
            ) as f:
                f.write(il_resources.read_text(resources, file_name))

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    def delete(self):
        with use_dir(Projects.BACKEND):
            log.info("Deleting command file")
            os.remove(os.path.join(Projects.BACKEND, "management", "commands", file_name))

    @property
    def installed(self):
        with use_dir(Projects.BACKEND):
            return os.path.exists(
                os.path.join(Projects.BACKEND, "management", "commands", file_name,),
            )


wait_command = WaitCommand()
