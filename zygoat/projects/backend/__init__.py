import os
import inspect
import importlib

from typing import Iterator
from docker.models.containers import Container

from zygoat.types import Path, Step
from zygoat.logging import log
from zygoat.constants import paths

from .settings import Settings
from . import steps

# TODO: untangle zygoat-django dependencies so we can drop this
_python_ver = ">=3.10,<4.0"

_exported_settings_values = [
    "ALLOWED_HOSTS",
    "DATABASES",
]

_run = "run"


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
    for step in _steps():
        step(python, project_path)

    # Finally, reformat our project to bring everything back inline
    python.zg_run("poetry run ruff format .", workdir=paths.B)


def _steps() -> Iterator[Step]:
    """
    Yields an iterator of Step functions discovered dynamically from .steps
    """

    # Get real path to our steps package
    base_dir = os.path.dirname(inspect.getfile(steps))

    # Walk the package file tree
    for root, dirs, files in os.walk(base_dir):
        # Only search the top level
        if root != base_dir:
            break
        for name in files:
            if ".py" not in name or "__init__" in name:
                continue

            module = importlib.import_module(
                f"{steps.__name__}.{os.path.splitext(name)[0]}",
            )
            if hasattr(module, _run):
                yield module.run
