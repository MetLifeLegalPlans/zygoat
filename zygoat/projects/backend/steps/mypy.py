import os

from zygoat.constants import BACKEND
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

from ..dependencies import Dependencies

_path = os.path.join(BACKEND, "mypy.ini")
_dev_deps = [
    "mypy",
    "django-stubs[compatible-mypy]",
]


def run(python: Container, project_path: Path) -> None:
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing mypy")
    dependencies.install(*_dev_deps, dev=True)

    log.info(f"Copying {_path}")
    resources.cp(_path)
