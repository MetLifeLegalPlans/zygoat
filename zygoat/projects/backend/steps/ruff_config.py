import os

from zygoat.resources import Resources

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_path = os.path.join(BACKEND, "ruff.toml")


def run(python: Container, project_path: Path):
    resources = Resources(project_path)

    log.info("Installing ruff config")
    resources.cp(_path)
