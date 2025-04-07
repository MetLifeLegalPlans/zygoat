from typing import cast
import os
import toml
from docker.models.containers import Container

from zygoat.types import Path
from zygoat.logging import log
from zygoat.constants import paths, BACKEND
from zygoat.utils import find_steps
from zygoat.resources import Resources

from .settings import Settings
from . import steps

_pyproject = "pyproject.toml"

# TODO: untangle zygoat-django dependencies so we can drop this
_python_ver = ">=3.10,<4.0"

_overridden_settings = [
    "ALLOWED_HOSTS",
    "DATABASES",
]
_settings_blocks = ["environment", "cache", "rest_framework"]


def generate(python: Container, project_path: Path):
    log.info("Starting backend generation")
    resources = Resources(project_path)

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
    data["tool"] = tool
    with open(pyproject_path, "w") as f:
        f.write(toml.dumps(data))

    # Perform settings modifications
    with Settings() as settings:
        for identifier in _overridden_settings:
            log.info(f"Removing default {identifier}")
            settings.remove_variable(identifier)

        # Assemble new settings block from resource files
        new_settings = "\n".join(
            [
                str(resources.read(os.path.join(BACKEND, "settings", f"{block}.py")))
                for block in _settings_blocks
            ]
            + ["\n"]  # Add a newline before the next comment in the file
        )
        settings.add_import(new_settings)  # Append to the end of the import block

    # Ready for dynamic step resolution!
    for step in find_steps(steps):
        step(python, project_path)

    # Finally, reformat our project to bring everything back inline
    python.zg_run_all(
        "poetry run ruff format .",
        "poetry run ruff check --fix .",
        workdir=paths.B,
    )
