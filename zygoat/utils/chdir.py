from typing import Callable

from zygoat.types import Path

import os

chdir: Callable

try:
    # Grab this from stdlib if we're on a version of Python that has it
    from contextlib import chdir as std_chdir

    chdir = std_chdir
except ImportError:
    # Otherwise implement our own shim for it
    from contextlib import contextmanager

    @contextmanager
    def _chdir(path: Path):
        """
        Backwards compatibility shim for contextlib.chdir
        """
        owd = os.getcwd()
        try:
            os.chdir(path)
            yield
        finally:
            os.chdir(owd)

    chdir = _chdir
