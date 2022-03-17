import logging
import os
import shutil

from .. import Component
from zygoat.utils.shell import multi_docker_run
from zygoat.constants import Projects

from .dockerfile import dockerfile
from .settings import settings
from .gitignore import gitignore
from .black import black
from .flake8 import flake8
from .banditrc import banditrc
from .pytest import pytest
from .dependencies import dependencies
from .reformat import reformat

log = logging.getLogger()


class Backend(Component):
    def create(self):
        log.info("Generating the django project")
        multi_docker_run(
            [
                [
                    "pip",
                    "install",
                    "--upgrade",
                    "django",
                ],
                [
                    "django-admin",
                    "startproject",
                    Projects.BACKEND,
                ],
            ],
            self.docker_image("PYTHON"),
            ".",
        )

        multi_docker_run(
            [
                [
                    "pip",
                    "install",
                    "--upgrade",
                    "pip",
                    "poetry",
                ],
                ["poetry", "init", "-n", "--name", "backend"],
            ],
            self.docker_image("PYTHON"),
            Projects.BACKEND,
        )

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
        gitignore,
        black,
        banditrc,
        flake8,
        pytest,
        # It is important that this comes last, so all relevant items can be reformatted
        reformat,
    ]
)
