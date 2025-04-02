from zygoat.types import Path
from zygoat.logging import log
from zygoat.resources import Resources

_files = [
    "Caddyfile",
    "docker-compose.yml",
]


def generate(project_path: Path):
    resources = Resources(project_path)
    for name in _files:
        log.info(f"Copying {name}")
        resources.cp(name)
