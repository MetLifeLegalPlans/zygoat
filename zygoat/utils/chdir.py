import os
from typing import Callable, Iterator

from zygoat.types import Path

chdir: Callable

try:
    # Grab this from stdlib if we're on a version of Python that has it
    from contextlib import chdir as std_chdir

    chdir = std_chdir
except ImportError:
    # Otherwise implement our own shim for it
    from contextlib import contextmanager

    @contextmanager
    def _chdir(path: Path) -> Iterator[None]:
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
