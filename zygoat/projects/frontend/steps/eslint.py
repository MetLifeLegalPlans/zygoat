import os

from zygoat.resources import Resources

from zygoat.constants import FRONTEND
from zygoat.types import Path, Container
from zygoat.logging import log

from ..dependencies import Dependencies
from ..package import Package

_plugins = [
    "import",
    "jest",
    "jsx-a11y",
    "prettier",
    "react",
    "react-hooks",
    "testing-library",
    "no-floating-promise",
]
_configs = [
    # Disabled for now, doesn't work with eslint 9
    # "airbnb",
    "prettier",
]

_dev_deps = [
    "eslint",
    *[f"eslint-plugin-{name}" for name in _plugins],
    *[f"eslint-config-{name}" for name in _configs],
    "globals",
    "@testing-library/dom",
    "@testing-library/react",
    "@testing-library/jest-dom",
]
_files = ["eslint.config.mjs"]

_prettier_glob = '"*/**/*.[jt]s?(x)"'


def run(node: Container, project_path: Path):
    dependencies = Dependencies(node)
    resources = Resources(project_path)

    log.info("Installing prettier")
    dependencies.install(*_dev_deps, dev=True)

    log.info("Adding lint scripts")
    with Package() as package:
        package.add_script("format", f"prettier --check {_prettier_glob}")
        package.add_script("fix", "npm run lint -- --fix && npm run format")

    log.info("Copying prettier config files")
    for name in _files:
        resources.cp(os.path.join(FRONTEND, name))
