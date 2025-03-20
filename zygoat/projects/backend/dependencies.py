from zygoat.utils.dependencies import AbstractDependenciesManager
from zygoat.constants import paths


class Dependencies(AbstractDependenciesManager):
    workdir = paths.BACKEND
    cmd_base = "poetry"
    dev_flag = ["--group", "dev"]


__all__ = [
    "Dependencies",
]
