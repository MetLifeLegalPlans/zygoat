import logging
import subprocess

from zygoat.components.base import Component


log = logging.getLogger()


class BaseDeployment(Component):
    def deployment_actions(self, env):
        raise NotImplementedError

    def deploy(self, env="staging", **kwargs):
        if not self.installed:
            log.info(f"{self.__class__.__name__} isn't installed, can't deploy")
            return

        self.deployment_actions(env, **kwargs)

    @property
    def commit_hash(self):
        return subprocess.check_output("git rev-parse HEAD", shell=True).decode().strip()
