from zygoat.logging import log
from zygoat.types import Container, Path

from ..dependencies import Dependencies

_prod_deps = [
    "prop-types",
    "axios",
    "js-cookie",
    "next-compose-plugins",
    "next-plugin-svgr",
    "next-images",
    "window-or-global",
]

_dev_deps = [
    "jest",
    "@axe-core/react",
    "css-mediaquery",
    "@types/js-cookie",
]


def run(node: Container, project_path: Path) -> None:
    dependencies = Dependencies(node)

    log.info("Installing prod dependencies")
    dependencies.install(*_prod_deps)

    log.info("Installing dev dependencies")
    dependencies.install(*_dev_deps, dev=True)
