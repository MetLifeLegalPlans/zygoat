import os
import toml
from docker.models.containers import Container

from zygoat.types import Path
from zygoat.logging import log
from zygoat.constants import paths, BACKEND
from zygoat.utils import find_steps

from .settings import Settings
from . import steps

_pyproject = "pyproject.toml"

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
    log.info(f"Generating a {_pyproject}")
    python.zg_run(f"poetry init -n --name backend --python '{_python_ver}'", workdir=paths.B)

    log.info(f"Setting package-mode=false in {_pyproject}")
    pyproject_path = os.path.join(BACKEND, _pyproject)
    with open(pyproject_path) as f:
        data = toml.load(f)

    # This section should be blank by default but future poetry updates
    # may change that
    tool = data.get("tool", {"poetry": {}})
    tool["poetry"]["package-mode"] = False
    with open(pyproject_path, "w") as f:
        f.write(toml.dumps(data))

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
