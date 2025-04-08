import requests

from zygoat.constants import GITIGNORE_URL, paths
from zygoat.logging import log
from zygoat.types import Container, Path

_static = """
# IntelliJ editors
.idea/

# Swap files
*.swp

# Virtual Environments
venv/
"""


def run(python: Container, project_path: Path):
    log.info("Fetching Python gitignore")
    res = requests.get(f"{GITIGNORE_URL}/python")
    res.raise_for_status()

    with open(paths.GITIGNORE, "a") as f:
        f.write(res.text)
        f.write(_static)
