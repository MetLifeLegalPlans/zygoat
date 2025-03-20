import shlex

from zygoat.utils.dependencies import AbstractDependenciesManager, Action
from zygoat.utils.commands import expand
from zygoat.constants import paths


class Dependencies(AbstractDependenciesManager):
    workdir = paths.FRONTEND
    cmd_base = "npm"

    install_cmd = "install"
    remove_cmd = "uninstall"

    dev_flag = "--save-dev"
    prod_flag = "--save"

    def _cmd(self, *packages, action: Action, dev=False) -> str:
        """
        Returns the command to install the packages
        """
        cmd = expand(self.cmd_base) + expand(getattr(self, f"{action.value}_cmd"))
        if dev:
            cmd += expand(self.dev_flag)
        else:
            cmd += expand(self.prod_flag)

        cmd += packages
        return shlex.join(cmd)


__all__ = [
    "Dependencies",
]
