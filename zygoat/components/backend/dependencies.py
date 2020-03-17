import logging

from zygoat.components import Component
from zygoat.constants import Phases
from zygoat.utils.backend import install_dependencies

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
        ]

        dev_dependencies = ["django-anymail", "pytz", "factory-boy", "flake8-black", "bandit"]

        log.info("Installing production dependencies")
        install_dependencies(*dependencies)

        log.info("Installing dev dependencies")
        install_dependencies(*dev_dependencies, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


dependencies = Dependencies()
