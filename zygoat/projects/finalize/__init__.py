from zygoat.logging import log
from zygoat.resources import Resources
from zygoat.types import Path

_files = [
    "Caddyfile",
    "docker-compose.yml",
    ".editorconfig",
    ".pre-commit-config.yaml",
]

_dirs = [".github"]


def generate(project_path: Path) -> None:
    resources = Resources(project_path)
    for name in _files:
        log.info(f"Copying {name}")
        resources.cp(name)

    for name in _dirs:
        log.info(f"Copying {name}")
        resources.cp(name, recursive=True)
