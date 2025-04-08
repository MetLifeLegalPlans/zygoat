import importlib
import inspect
import os
from typing import Iterator

from zygoat.types import Step

_run = "run"


def find_steps(pkg) -> Iterator[Step]:
    """
    Yields an iterator of run(container, project_path) functions discovered
    dynamically from pkg
    """

    # Get real path to our steps package
    base_dir = os.path.dirname(inspect.getfile(pkg))

    # Walk the package file tree
    for root, dirs, files in os.walk(base_dir):
        # Only search the top level
        if root != base_dir:
            break
        for name in files:
            if ".py" not in name or "__init__" in name:
                continue

            module = importlib.import_module(
                f"{pkg.__name__}.{os.path.splitext(name)[0]}",
            )
            if hasattr(module, _run):
                yield module.run
