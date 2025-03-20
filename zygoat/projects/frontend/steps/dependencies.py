from zygoat.types import Path, Container
from zygoat.logging import log

from ..dependencies import Dependencies

_prod_deps = [
    "prop-types",
    "axios",
    "next-compose-plugins",
    "next-plugin-svgr",
    "next-images",
    "window-or-global",
]

_dev_deps = [
    "jest",
    "@axe-core/react",
    "@testing-library/dom",
    "@testing-library/react",
    "@testing-library/jest-dom",
    "css-mediaquery",
]


def run(node: Container, project_path: Path):
    dependencies = Dependencies(node)

    log.info("Installing prod dependencies")
    dependencies.install(*_prod_deps)

    log.info("Installing dev dependencies")
    dependencies.install(*_dev_deps, dev=True)
