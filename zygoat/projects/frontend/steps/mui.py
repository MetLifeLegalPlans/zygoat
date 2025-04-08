import os

from zygoat.constants import FRONTEND
from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Container, Path

from ..dependencies import Dependencies

_prod_deps = [
    "@mui/material",
    "@mui/material-nextjs",
    "@emotion/react",
    "@emotion/cache",
    "@emotion/styled",
]

_files = ["app/layout.tsx", "theme.ts"]


def run(node: Container, project_path: Path):
    dependencies = Dependencies(node)
    resources = Resources(project_path)

    log.info("Installing MUI dependencies")
    dependencies.install(*_prod_deps)

    for name in _files:
        path = os.path.join(FRONTEND, name)
        log.info(f"Copying {path}")
        resources.cp(path)
