import os

from zygoat.constants import BACKEND, paths
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

_path = os.path.join(BACKEND, paths.GUNICORN_CONF)


def run(python: Container, project_path: Path) -> None:
    resources = Resources(project_path)
    log.info(f"Copying {_path}")
    resources.cp(_path)
