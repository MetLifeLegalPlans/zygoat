import logging
import os
import shutil

from zygoat.components import Component
from zygoat.constants import Projects, Phases
from zygoat.utils.shell import run
from zygoat.utils.files import use_dir

from .dockerfile import dockerfile
from .gitignore import gitignore
from .prettier import prettier
from .eslint import eslint
from .cypress import cypress
from .next_config import next_config
from .dependencies import dependencies
from .jsconfig import js_config

log = logging.getLogger()


class Frontend(Component):
    def create(self):
        log.info("Installing/upgrading yarn through npm")
        run(["npm", "install", "-g", "--upgrade", "yarn"])

        log.info("Running create-next-app")
        run(["yarn", "create", "next-app", Projects.FRONTEND])

        log.info("Emptying a poorly formatted index.js file")
        open(os.path.join(Projects.FRONTEND, "pages", "index.js"), "w").close()

        log.info("Deleting default _app.js file (added in create-next-app v9.5.5)")
        os.remove(os.path.join(Projects.FRONTEND, "pages", "_app.js"))

        log.info("Deleting the default api directory")
        shutil.rmtree(os.path.join(Projects.FRONTEND, "pages", "api"))

    def delete(self):
        log.warning(f"Deleting the {Projects.FRONTEND} project")
        shutil.rmtree(Projects.FRONTEND)

    @property
    def installed(self):
        return os.path.exists(Projects.FRONTEND)


class Reformat(Component):
    def create(self):
        log.info("Formatting package.json with prettier")
        with use_dir(Projects.FRONTEND):
            run(["yarn", "prettier", "-w", "package.json"])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        # json.dump does not do a good job of preserving formatting
        with open(os.path.join(Projects.FRONTEND, "package.json")) as f:
            return "\n" in f.read()


frontend = Frontend(
    sub_components=[
        dockerfile,
        gitignore,
        prettier,
        dependencies,
        eslint,
        cypress,
        next_config,
        js_config,
        Reformat(),
    ]
)
