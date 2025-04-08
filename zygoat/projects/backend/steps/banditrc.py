import os

from zygoat.constants import BACKEND
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

_path = os.path.join(BACKEND, "tests")
_name = ".banditrc"


def run(python: Container, project_path: Path):
    log.info(f"Adding {_name}")
    resources = Resources(project_path)
    os.makedirs(_path)
    resources.cp(os.path.join(_path, _name))
