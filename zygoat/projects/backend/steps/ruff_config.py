import os

from zygoat.constants import BACKEND
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

from ..dependencies import Dependencies

_path = os.path.join(BACKEND, "ruff.toml")


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing ruff")
    dependencies.install("ruff", dev=True)

    log.info(f"Copying {_path}")
    resources.cp(_path)
