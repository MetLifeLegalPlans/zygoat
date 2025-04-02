import os
from zygoat.resources import Resources

from zygoat.constants import FRONTEND
from zygoat.types import Path, Container
from zygoat.logging import log

from ..dependencies import Dependencies

_deps = ["@sentry/nextjs"]
_files = [
    "next.config.ts",
    "zygoat.next.config.js",
    "instrumentation.ts",
    "instrumentation-client.ts",
    "app/global-error.tsx",
]

_sentry_pattern = "sentry.{}.config.ts"
_files += [_sentry_pattern.format(conf) for conf in ("server", "edge")]


def run(node: Container, project_path: Path):
    dependencies = Dependencies(node)
    resources = Resources(project_path)

    log.info("Installing Sentry package")
    dependencies.install(*_deps)

    for name in _files:
        path = os.path.join(FRONTEND, name)
        log.info(f"Copying {path}")
        resources.cp(path)
