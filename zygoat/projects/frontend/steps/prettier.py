import os

from zygoat.constants import FRONTEND
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

from ..dependencies import Dependencies
from ..package import Package

_prettier = "prettier"
_dev_deps = [_prettier, "@trivago/prettier-plugin-sort-imports"]
_files = [".prettierrc", ".prettierignore"]


def run(node: Container, project_path: Path) -> None:
    dependencies = Dependencies(node)
    resources = Resources(project_path)

    log.info("Installing prettier")
    dependencies.install(*_dev_deps, dev=True)

    log.info("Adding format script")
    with Package() as package:
        package.add_script("format", "prettier --write .")

    for name in _files:
        path = os.path.join(FRONTEND, name)
        log.info(f"Copying {path}")
        resources.cp(path)
