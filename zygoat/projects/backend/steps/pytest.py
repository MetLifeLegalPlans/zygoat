import os

from zygoat.resources import Resources
from ..dependencies import Dependencies

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_path = os.path.join(BACKEND, "pytest.ini")
_dev_deps = [
    "pytest",
    "pytest-django",
    "pytest-cov",
]


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing Pytest dependencies")
    dependencies.install(*_dev_deps, dev=True)

    log.info("Copying pytest.ini")
    resources.cp(_path)
