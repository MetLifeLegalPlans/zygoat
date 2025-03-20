import os

from zygoat.resources import Resources
from ..dependencies import Dependencies

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_path = os.path.join(BACKEND, "ruff.toml")


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing ruff")
    dependencies.install("ruff", dev=True)

    log.info(f"Copying {_path}")
    resources.cp(_path)
