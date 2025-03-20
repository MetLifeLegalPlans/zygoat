import os

from zygoat.resources import Resources

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND, paths


def run(python: Container, project_path: Path):
    resources = Resources(project_path)

    for dockerfile in paths.dockerfiles:
        path = os.path.join(BACKEND, dockerfile)
        log.info(f"Copying {dockerfile}")
        resources.cp(path)
