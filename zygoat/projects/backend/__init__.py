from docker.models.containers import Container

from zygoat.types import Path
from zygoat.logging import log
from zygoat.constants import paths
from zygoat.utils import find_steps

from .settings import Settings
from . import steps

# TODO: untangle zygoat-django dependencies so we can drop this
_python_ver = ">=3.10,<4.0"

_exported_settings_values = [
    "ALLOWED_HOSTS",
    "DATABASES",
]


def generate(python: Container, project_path: Path):
    log.info("Starting backend generation")

    # Collect basic dependencies and generate project
    log.info("Installing pip, poetry, and generating the Django project")
    python.zg_run_all(
        "pip install --upgrade pip",  # Run on its own so the new resolver can be used for future dependencies
        "pip install --upgrade django poetry",
        "django-admin startproject backend",
    )

    # Initialize pyproject.toml
    log.info("Generating a pyproject.toml")
    python.zg_run(f"poetry init -n --name backend --python '{_python_ver}'", workdir=paths.B)

    # Perform settings modifications
    with Settings() as settings:
        log.info("Creating import for zygoat-django settings")
        settings.add_import("from zygoat_django.settings import *")

        for identifier in _exported_settings_values:
            log.info(f"Removing default {identifier}")
            settings.remove_variable(identifier)

    # Ready for dynamic step resolution!
    for step in find_steps(steps):
        step(python, project_path)

    # Finally, reformat our project to bring everything back inline
    python.zg_run("poetry run ruff format .", workdir=paths.B)
