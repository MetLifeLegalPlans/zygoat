from functools import partial
import os
from shutil import copy, copytree
from typing import Optional

import importlib_resources

from zygoat.types import Path


class Resources:
    project_path: Path

    def __init__(self, project_path: Path):
        self.project_path = project_path

    @property
    def pkg(self):
        return importlib_resources.files("zygoat.resources")

    def cp(self, path: Path, recursive=False, dest: Optional[str] = None):
        """
        Copies a file or directory from the resources package. By default it
        copies the data to the same path in the generated projected, e.g.

        >>> r = Resources("/home/user/project")
        >>> r.cp("backend/Dockerfile.local")

        Copies zygoat/resources/backend/Dockerfile.local to
        /home/user/project/backend/Dockerfile.local
        """
        pkg = self.pkg  # Shorthand alias

        src_path = os.path.join(pkg, path)
        dest_path = os.path.join(
            self.project_path,
            dest
            if dest is not None
            else path,  # Mirror the path onto the generated project by default
        )

        cp = partial(copytree, dirs_exist_ok=True) if recursive else copy
        return cp(src_path, dest_path)
