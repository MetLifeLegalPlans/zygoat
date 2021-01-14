import logging
import os

from zygoat.components import Component
from zygoat.constants import Phases, Projects
from zygoat.utils.backend import install_dependencies, dev_file_name, prod_file_name

log = logging.getLogger()


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
            "uvicorn",
        ]

        dev_dependencies = ["pytz", "factory-boy", "flake8-black", "bandit"]

        log.info("Installing production dependencies")
        install_dependencies(*dependencies, extras={"uvicorn": ["standard"]})

        log.info("Installing dev dependencies")
        install_dependencies(*dev_dependencies, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @property
    def installed(self):
        paths = [os.path.join(Projects.BACKEND, p) for p in [prod_file_name, dev_file_name]]

        for path in paths:
            if not os.path.exists(path):
                return False

        return True


dependencies = Dependencies()
