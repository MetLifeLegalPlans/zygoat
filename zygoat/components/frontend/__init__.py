import logging
import os
import shutil

from zygoat.components import Component
from zygoat.constants import Projects
from zygoat.utils.shell import run

from .dockerfile import dockerfile
from .gitignore import gitignore
from .prettier import prettier
from .eslint import eslint
from .cypress import cypress
from .next_config import next_config
from .proxy import proxy
from .dependencies import dependencies

log = logging.getLogger()


class Frontend(Component):
    def create(self):
        log.info("Installing/upgrading yarn through npm")
        run(["npm", "install", "-g", "--upgrade", "yarn"])

        log.info("Running create-next-app")
        run(["yarn", "create", "next-app", Projects.FRONTEND])

        log.info("Deleting a poorly formatted index page")
        open(os.path.join(Projects.FRONTEND, "pages", "index.js"), "w").close()

    def delete(self):
        log.warning(f"Deleting the {Projects.FRONTEND} project")
        shutil.rmtree(Projects.FRONTEND)

    @property
    def installed(self):
        return os.path.exists(Projects.FRONTEND)


frontend = Frontend(
    sub_components=[
        dockerfile,
        gitignore,
        prettier,
        dependencies,
        eslint,
        cypress,
        next_config,
        proxy,
    ]
)
