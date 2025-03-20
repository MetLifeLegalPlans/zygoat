import os

from zygoat.resources import Resources

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import FRONTEND, paths


def run(node: Container, project_path: Path):
    resources = Resources(project_path)

    for dockerfile in paths.dockerfiles:
        path = os.path.join(FRONTEND, dockerfile)
        log.info(f"Copying {dockerfile}")
        resources.cp(path)
