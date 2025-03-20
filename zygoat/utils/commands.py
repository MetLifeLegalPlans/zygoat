import shlex
from typing import List

from zygoat.types import Command


def expand(cmd: Command) -> List[str]:
    """
    Expands a command string into a list, or returns cmd if cmd is already
    a list
    """
    if isinstance(cmd, str):
        return shlex.split(cmd)
    return cmd
