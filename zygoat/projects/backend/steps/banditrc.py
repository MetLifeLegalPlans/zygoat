import os

from zygoat.resources import Resources

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_path = os.path.join(BACKEND, "tests")
_name = ".banditrc"


def run(python: Container, project_path: Path):
    log.info(f"Adding {_name}")
    resources = Resources(project_path)
    os.makedirs(_path)
    resources.cp(os.path.join(_path, _name))
