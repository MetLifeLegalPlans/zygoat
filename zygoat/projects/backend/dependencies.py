from zygoat.constants import paths
from zygoat.utils.dependencies import AbstractDependenciesManager


class Dependencies(AbstractDependenciesManager):
    """
    Dependency manager that interacts with poetry via docker

    >>> from zygoat.container_ext import spawn
    >>> python = spawn('python:latest')  # See zygoat.container_ext for details
    >>>
    >>> dependencies = Dependencies(python)
    >>> dependencies.install("django", "dramatiq", "django-apscheduler")
    ...output snipped
    >>> dependencies.install("ruff", "pytest", dev=True)
    """

    workdir = paths.BACKEND
    cmd_base = "poetry"
    dev_flag = ["--group", "dev"]


__all__ = [
    "Dependencies",
]
