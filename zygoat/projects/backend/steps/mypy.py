import os

from zygoat.resources import Resources
from ..dependencies import Dependencies

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_path = os.path.join(BACKEND, "mypy.ini")


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing mypy")
    dependencies.install("mypy", dev=True)

    log.info(f"Copying {_path}")
    resources.cp(_path)
