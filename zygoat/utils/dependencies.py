from enum import Enum
from typing import List, Any
import shlex
from docker.models.containers import Container

from zygoat.types import Path, Command
from .commands import expand


class Action(Enum):
    INSTALL = "install"
    REMOVE = "remove"


class AbstractDependenciesManager:
    """
    Generic implementation of a dependency manager. Each project should
    make its own subclass of this that specifies workdir, cmd_base, and dev_flag
    """

    container: Container
    workdir: Path

    cmd_base: Command
    dev_flag: Command

    # Commands corresponding to Action enum types
    # Default values are for Poetry
    install_cmd: Command = "add"
    remove_cmd: Command = "remove"

    @property
    def required_overrides(self) -> List[Any]:
        return ["workdir", "dev_flag", "cmd_base"]

    def __init__(self, container: Container):
        if any([getattr(self, name, None) is None for name in self.required_overrides]):
            raise NotImplementedError("Required class members not set!")

        self.container = container

    def _cmd(self, *packages, action: Action, dev=False) -> str:
        """
        Returns the command to install the packages
        """
        cmd = expand(self.cmd_base) + expand(getattr(self, f"{action.value}_cmd"))
        if dev:
            cmd += expand(self.dev_flag)

        cmd += packages

        return shlex.join(cmd)

    def install(self, *packages, dev=False):
        """
        Adds dependencies
        """
        return self.container.zg_run(
            self._cmd(*packages, action=Action.INSTALL, dev=dev),
            workdir=self.workdir,
        )

    def remove(self, *packages, dev=False):
        """
        Removes dependencies
        """
        return self.container.zg_run(
            self._cmd(*packages, action=Action.REMOVE, dev=dev),
            workdir=self.workdir,
        )
