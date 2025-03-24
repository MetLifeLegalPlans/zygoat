from typing import Dict, Any

import json

from zygoat.constants import paths
from zygoat.types import Path

_scripts = "scripts"


class Package:
    """
    Provides a handful of utilities for accessing and modifying
    a NodeJS package.json file. For use as a context manager -

    >>> with Package(path_to_settings) as package:
    ...     package.add_script("name", "command --to run")

    See method docstrings for usage information.
    """

    data: Dict[str, Any]
    path: Path

    def __init__(self, path: Path = paths.PACKAGE):
        self.path = path

    def add_script(self, name: str, cmd: str):
        """
        Adds a new script.

        >>> package.add_script("format", "prettier --write .")
        """
        p = self.data
        p["scripts"][name] = cmd

    @property
    def raw(self) -> str:
        """
        The formatted string representation of the package file.
        """
        return json.dumps(self.data, indent=2)

    def _load(self):
        """
        Loads the package from file into memory.
        """
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def _dump(self):
        """
        Dumps the package from memory to file.
        """
        # First make sure that we have a valid AST before clearing file contents
        assert self.raw is not None

        # THEN write
        with open(self.path, "w") as f:
            f.write(self.raw)

    def __enter__(self):
        self._load()
        return self

    def __exit__(self, *args):
        self._dump()
