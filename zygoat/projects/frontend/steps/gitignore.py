import requests

from zygoat.constants import GITIGNORE_URL, paths
from zygoat.logging import log
from zygoat.types import Container, Path

_static = """
# Used by some language servers
.tern-port
"""


def run(node: Container, project_path: Path):
    log.info("Fetching Node gitignore")
    res = requests.get(f"{GITIGNORE_URL}/node")
    res.raise_for_status()

    with open(paths.GITIGNORE, "a") as f:
        f.write(res.text)
        f.write(_static)
