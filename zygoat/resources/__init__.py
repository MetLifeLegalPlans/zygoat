"""
.. include:: ../../RESOURCES.md
  :start-line: 2
"""

from functools import partial
import os
from shutil import copy, copytree
from typing import Optional, Literal, overload, Union, Any

from pathlib import PosixPath
from importlib import resources
import importlib

from zygoat.types import Path


class Resources:
    """
    Exposes some helper methods for copying files between zygoat and your project.
    """

    project_path: Path

    def __init__(self, project_path: Path):
        """
        Initializes a resource object, where `project_path` is the path to your project.
        """
        self.project_path = project_path

    def cp(self, path: Path, recursive: bool = False, dest: Optional[str] = None) -> Any:
        """
        Copies a file or directory from the resources package. By default it
        copies the data to the same path in the generated projected, e.g.
        >>> r = Resources("/home/user/project")
        >>> r.cp("backend/Dockerfile.local")

        Copies zygoat/resources/backend/Dockerfile.local to
        /home/user/project/backend/Dockerfile.local

        You can also control the destination -
        >>> r.cp("backend/Dockerfile", dest="backend/Dockerfile.prod")

        And copy directories -
        >>> r.cp(".github", recursive=True)
        """
        pkg = self.pkg  # Shorthand alias

        # Traversable implements just enough of PathLike for join to work
        # despite the more specific type on os.path.join
        src_path = os.path.join(pkg, path)  # type: ignore
        dest_path = os.path.join(
            self.project_path,
            dest
            if dest is not None
            else path,  # Mirror the path onto the generated project by default
        )

        cp = partial(copytree, dirs_exist_ok=True) if recursive else copy
        return cp(src_path, dest_path)

    @overload
    def read(self, path: Path) -> str: ...
    @overload
    def read(self, path: Path, binary: bool = ...) -> bytes: ...

    def read(self, path: Path, binary: bool = False) -> Union[str, bytes]:
        """
        Reads a file from the resources package. By default it returns
        the contents as text, but this can be controlled with the binary
        flag.

        >>> r.read("backend/pytest.ini")
        "pytest_ini_contents..."
        >>> r.read("backend/pytest.ini", binary=True)
        b"pytest_ini_contents..."
        """

        pkg = self.pkg
        mode = "rb" if binary else "r"
        # See L49
        with open(os.path.join(pkg, path), mode) as f:  # type: ignore
            return f.read()  # type: ignore

    @property
    def pkg(self) -> importlib.abc.Traversable:
        return resources.files("zygoat.resources")
