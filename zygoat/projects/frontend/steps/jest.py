import os

from zygoat.resources import Resources
from zygoat.constants import FRONTEND
from zygoat.types import Path, Container
from zygoat.logging import log

from ..dependencies import Dependencies
from ..package import Package

_dev_deps = ["jest", "next-router-mock", "jest-environment-jsdom"]


def run(node: Container, project_path: Path):
    dependencies = Dependencies(node)
    resources = Resources(project_path)

    log.info("Installing jest packages")
    dependencies.install(*_dev_deps, dev=True)

    log.info("Adding jest test commands")
    with Package() as package:
        package.add_script("test", "jest --passWithNoTests")
        package.add_script("test-coverage", "jest --coverage --passWithNoTests")

    log.info("Copying jest configuration files")
    for infix in ["setup", "config"]:
        resources.cp(os.path.join(FRONTEND, f"jest.{infix}.js"))
