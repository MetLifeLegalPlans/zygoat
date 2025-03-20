from docker.models.containers import Container

from zygoat.types import Path
from zygoat.logging import log
from zygoat.constants import paths

from ..settings import Settings
from ..dependencies import Dependencies
from zygoat.resources import Resources

_prod_deps = [
    "Django",
    "psycopg2-binary",
    "django-cors-headers",
    "djangorestframework",
    "django-environ",
    "djangorestframework-camel-case",
    "django-anymail",
    "zygoat-django",
    "gunicorn[gevent]",
    "uvicorn[standard]",
    "psycogreen",
]

_dev_deps = [
    "pytz",
    "factory-boy",
    "flake8-black",
    "bandit",
]


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)

    log.info("Installing prod dependencies")
    dependencies.install(*_prod_deps)

    log.info("Installing dev dependencies")
    dependencies.install(*_dev_deps, dev=True)
