import os

from zygoat.resources import Resources
from ..dependencies import Dependencies

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_pytest_path = os.path.join(BACKEND, "pytest.ini")
_dev_deps = [
    "pytest",
    "pytest-django",
    "pytest-cov",
    "pytest-xdist",
]


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing Pytest dependencies")
    dependencies.install(*_dev_deps, dev=True)

    log.info("Copying pytest.ini")
    resources.cp(_pytest_path)

    log.info("Copying placeholder test so pytest doesn't immediately fail")
    resources.cp(os.path.join(BACKEND, "tests", "test_placeholder.py"))
