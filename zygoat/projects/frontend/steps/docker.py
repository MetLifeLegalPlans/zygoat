import os

from zygoat.constants import FRONTEND, paths
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path


def run(node: Container, project_path: Path) -> None:
    resources = Resources(project_path)

    for dockerfile in paths.dockerfiles:
        path = os.path.join(FRONTEND, dockerfile)
        log.info(f"Copying {dockerfile}")
        resources.cp(path)
