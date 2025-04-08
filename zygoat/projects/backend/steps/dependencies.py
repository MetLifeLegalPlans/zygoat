from zygoat.logging import log
from zygoat.types import Container, Path

from ..dependencies import Dependencies

_prod_deps = [
    "Django",
    "psycopg2-binary",
    "django-cors-headers",
    "djangorestframework",
    "django-environ",
    "djangorestframework-camel-case",
    "django-anymail",
    "django-redis",
    "gunicorn[gevent]",
    "uvicorn[standard]",
    "psycogreen",
    "django-willing-zg",
]

_dev_deps = [
    "pytz",
    "factory-boy",
    "bandit",
]


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)

    log.info("Installing prod dependencies")
    dependencies.install(*_prod_deps)

    log.info("Installing dev dependencies")
    dependencies.install(*_dev_deps, dev=True)
