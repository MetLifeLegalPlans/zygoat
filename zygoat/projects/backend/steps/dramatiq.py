import os

from zygoat.constants import BACKEND
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

from ..dependencies import Dependencies
from ..settings import Settings

_dependencies = [
    "dramatiq[redis]",  # Base task queue
    "django-dramatiq",  # Task queue integration into Django
    "apscheduler",  # Scheduling service for tasks
    "django-apscheduler",  # Scheduler integration into Django
]


def run(python: Container, project_path: Path) -> None:
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing dramatiq+apscheduler dependencies")
    dependencies.install(*_dependencies)

    with Settings() as settings:
        log.info("Adding dramatiq+apscheduler to INSTALLED_APPS")
        settings.add_installed_app("'django_dramatiq'", prepend=True)
        settings.add_installed_app("'django_apscheduler'")

        log.info("Adding dramatiq config to settings")
        settings.append(resources.read(os.path.join(BACKEND, "settings", "dramatiq.py")))
