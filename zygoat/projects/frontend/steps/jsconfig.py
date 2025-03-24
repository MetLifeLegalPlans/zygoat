from zygoat.resources import Resources

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import paths


def run(node: Container, project_path: Path):
    resources = Resources(project_path)
    log.info(f"Copying {paths.TSCONFIG}")
    resources.cp(paths.TSCONFIG)
