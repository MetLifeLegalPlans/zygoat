import os

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import FRONTEND

from zygoat.resources import Resources
from ..dependencies import Dependencies

_prod_deps = [
    "@mui/material",
    "@mui/material-nextjs",
    "@emotion/react",
    "@emotion/cache",
    "@emotion/server",
    "@emotion/styled",
]

_files = [
    "pages/_app.js",
    "pages/_document.js",
]


def run(node: Container, project_path: Path):
    dependencies = Dependencies(node)
    resources = Resources(project_path)

    log.info("Installing MUI dependencies")
    dependencies.install(*_prod_deps)

    for name in _files:
        path = os.path.join(FRONTEND, name)
        log.info(f"Copying {path}")
        resources.cp(path)
