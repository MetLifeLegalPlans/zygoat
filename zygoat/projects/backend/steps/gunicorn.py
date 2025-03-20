import os

from zygoat.resources import Resources

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND, paths

_path = os.path.join(BACKEND, paths.GUNICORN_CONF)


def run(python: Container, project_path: Path):
    resources = Resources(project_path)
    log.info(f"Copying {_path}")
    resources.cp(_path)
