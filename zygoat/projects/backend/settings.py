from typing import Optional

import shlex

from zygoat.constants import paths
from zygoat.types import Path

from redbaron import RedBaron


class Settings:
    """
    Provides a handful of utilities for accessing and modifying
    a Django settings.py file. For use as a context manager -

    >>> with SettingsManager(path_to_settings) as settings:
    ...     settings.add_import("from zygoat_django.settings import *")
    ...     settings

    See method docstrings for usage information.
    """

    red: RedBaron
    path: Path

    def __init__(self, path: Path = paths.SETTINGS):
        self.path = path

    def wrap_secret_key(self):
        r = self.red
        key_statement = r.find("name", value="SECRET_KEY").parent

        # Get the actual secret key
        current = str(key_statement.value)

        # Wrap it as a prod_required_env
        r[key_statement.index_on_parent] = (
            f"SECRET_KEY = prod_required_env('DJANGO_SECRET_KEY', default={current})"
        )

    def append(self, line: str):
        """
        Appends a new line to the end of the file.

        >>> settings.append("env = environ.Env()")
        """
        r = self.red

        r.append(line)

    def add_import(self, line: str):
        """
        Appends a new line to the import block.

        >>> settings.add_import("from zygoat_django.settings import *")
        >>> settings.add_import("import sys")
        """
        r = self.red

        # Find all imports in the
        imports = r.find_all("FromImportNode") + r.find_all("ImportNode")
        last_import = max([node.index_on_parent for node in imports]) + 1
        pre = r[:last_import]
        new = RedBaron(line)
        post = r[last_import:]

        pre.extend(new)
        pre.extend(post)
        self.red = pre

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
        apps = r.find("name", value="INSTALLED_APPS").parent.value

        if position is not None:
            return apps.insert(position, app)
        if prepend:
            return apps.insert(0, app)
        return apps.append(app)

    def remove_variable(self, name: str):
        """
        Removes an identifier from the settings file. Mostly useful for
        removing defaults for variables exported from zygoat_django
        """
        # red.find => NameNode, .parent => AssignmentNode
        idx = self.red.find("name", value=name).parent.index_on_parent
        del self.red[idx]

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
