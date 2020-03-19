import logging
import os
import shutil

from .. import Component
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run
from zygoat.constants import Projects, VENV

from .dockerfile import dockerfile
from .wait_command import wait_command
from .settings import settings
from .gitignore import gitignore
from .black import black
from .flake8 import flake8
from .banditrc import banditrc
from .dependencies import dependencies
from .reformat import reformat

log = logging.getLogger()


class Backend(Component):
    def create(self):
        log.info("Installing django at a user level to generate the project")
        run(["pip", "install", "--user", "--upgrade", "django"])

        log.info("Creating the django project")
        run(["django-admin", "startproject", Projects.BACKEND])

        with use_dir(Projects.BACKEND):
            log.info("Creating a virtualenv for the project")
            run(["virtualenv", VENV])

    def update(self):
        pass

    def delete(self):
        log.warning(f"Deleting the {Projects.BACKEND} project")
        shutil.rmtree(Projects.BACKEND)

    @property
    def installed(self):
        return os.path.exists(Projects.BACKEND)


backend = Backend(
    sub_components=[
        settings,
        dockerfile,
        dependencies,
        wait_command,
        gitignore,
        black,
        banditrc,
        flake8,
        # It is important that this comes last, so all relevant items can be reformatted
        reformat,
    ]
)
