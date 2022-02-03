import logging
import os

from zygoat.components import Component
from zygoat.constants import Phases, Projects
from zygoat.utils.backend import install_dependencies

log = logging.getLogger()

project_file_name = "pyproject.toml"
lock_file_name = "poetry.lock"


class Dependencies(Component):
    def create(self):
        dependencies = [
            "Django",
            "psycopg2-binary",
            "django-cors-headers",
            "djangorestframework",
            "django-environ",
            "djangorestframework-camel-case",
            "django-anymail",
            "zygoat-django",
            "gunicorn",
            "uvicorn[standard]",
        ]

        dev_dependencies = ["pytz", "factory-boy", "flake8-black", "bandit"]

        log.info("Installing production dependencies")
        install_dependencies(*dependencies)

        log.info("Installing dev dependencies")
        install_dependencies(*dev_dependencies, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        paths = [
            os.path.join(Projects.BACKEND, p) for p in [project_file_name, lock_file_name]
        ]

        for path in paths:
            if not os.path.exists(path):
                return False

        return True


dependencies = Dependencies()
