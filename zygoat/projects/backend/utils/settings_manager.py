from typing import Union, Optional

import os
import shlex

from redbaron import RedBaron


class SettingsManager:
    """
    Provides a handful of utilities for accessing and modifying
    a Django settings.py file. For use as a context manager -

    >>> with SettingsManager(path_to_settings) as settings:
    ...     settings.add_import("from zygoat_django.settings import *")
    ...     settings

    See method docstrings for usage information.
    """

    red: RedBaron
    path: Union[os.PathLike, str]

    def __init__(self, path: Union[os.PathLike, str]):
        self.path = path

    def add_import(self, line: str):
        """
        Appends a new line to the import block.

        >>> settings.add_import("from zygoat_django.settings import *")
        >>> settings.add_import("import sys")
        """
        r = self.red

        # Find all imports in the
        imports = r.find_all("FromImportNode") + r.find_all("ImportNode")
        last_import = max([node.index_on_parent for node in imports])
        r.insert(last_import + 1, line)

    def add_installed_app(
        self,
        app: str,
        prepend: bool = False,
        position: Optional[int] = None,
    ):
        """
        Adds a new app name to INSTALLED_APPS. Defaults to appending,
        but accepts either a prepend flag or specific position

        >>> settings.add_installed_app("backend")
        >>> settings.add_installed_app("django_dramatiq", prepend=True)
        >>> settings.add_installed_app("unfold", position=1)
        """
        r = self.red

        # Quote the string if not already so it is interpreted as a string value
        # and not a variable. For INSTALLED_APPS specifically this is sane,
        # for other lists we want the caller to quote explicitly if required
        app = shlex.quote(app)
        apps = r.find("name", value="INSTALLED_APPS").parent.value

        if position is not None:
            return apps.insert(position, app)
        if prepend:
            return apps.insert(0, app)
        return apps.append(app)

    @property
    def raw(self) -> str:
        """
        The raw string representation of the AST. Mostly useful for testing,
        not recommended for use in project generation.
        """
        return self.red.dumps()

    def _load(self):
        """
        Loads the AST from file into memory.
        """
        with open(self.path, "r") as f:
            self.red = RedBaron(f.read())

    def _dump(self):
        """
        Dumps the AST from memory to file.
        """
        # First make sure that we have a valid AST before clearing file contents
        assert self.red.dumps() is not None

        # THEN write
        with open(self.path, "w") as f:
            f.write(self.raw)

    def __enter__(self):
        self._load()
        return self

    def __exit__(self, *args):
        self._dump()
