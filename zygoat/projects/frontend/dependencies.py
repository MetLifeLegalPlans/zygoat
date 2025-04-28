import shlex

from zygoat.constants import paths
from zygoat.utils.commands import expand
from zygoat.utils.dependencies import AbstractDependenciesManager, Action


class Dependencies(AbstractDependenciesManager):
    """
    Dependency manager that interacts with NPM via docker

    >>> from zygoat.container_ext import spawn
    >>> node = spawn('node:latest')  # See zygoat.container_ext for details
    >>> dependencies = Dependencies(node)
    >>> dependencies.install("@mui/material", "@mui/material-nextjs")
    ...output snipped
    >>> dependencies.install("jest", "next-router-mock", dev=True)
    """

    workdir = paths.FRONTEND
    cmd_base = "npm"

    install_cmd = "install"
    remove_cmd = "uninstall"

    dev_flag = "--save-dev"
    prod_flag = "--save"

    def _cmd(self, *packages: str, action: Action, dev: bool = False) -> str:
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
