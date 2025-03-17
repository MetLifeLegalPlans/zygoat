from docker.models.containers import Container
from zygoat.logging import log
from zygoat.constants import paths

from .utils.settings_manager import SettingsManager

_exported_settings_values = [
    "ALLOWED_HOSTS",
    "DATABASES",
]


def generate(python: Container = None, node: Container = None):
    log.info("Starting backend generation")

    log.info("Installing pip, poetry, and django")
    python.zg_run_all(
        "pip install --upgrade pip",  # Run on its own so the new resolver can be used for future dependencies
        "pip install --upgrade django poetry",
        "django-admin startproject backend",
    )

    log.info("Generating the Django project")
    python.zg_run("poetry init -n --name backend", workdir=paths.B)

    with SettingsManager() as settings:
        log.info("Creating import for zygoat-django settings")
        settings.add_import("from zygoat_django.settings import *")

        for identifier in _exported_settings_values:
            log.info(f"Removing default {identifier}")
            settings.remove_variable(identifier)
