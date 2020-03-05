import logging

from zygoat.components import Component
from zygoat.constants import Phases
from zygoat.utils.backend import install_dependency

log = logging.getLogger()


class Dependencies(Component):
    def create(self):
        dependencies = [
            "Django",
            "psycopg2-binary",
            "django-cors-headers",
            "djangorestframework",
            "django-environ",
        ]

        dev_dependencies = ["django-anymail", "pytz", "factory-boy"]

        log.info("Installing production dependencies")
        install_dependency(*dependencies)

        log.info("Installing dev depencies")
        install_dependency(*dev_dependencies, dev=True)

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


dependencies = Dependencies()
