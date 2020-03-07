import logging
import subprocess

from zygoat.components.base import Component


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class BaseDeployment(Component):
    @property
    def should_deploy(self):
        return True

    def deployment_actions(self, env):
        raise NotImplementedError

    def deploy(self, env="staging"):
        if not self.should_deploy:
            log.info(f"{self.__class__.__name__} should not deploy, skipping")
            return

        if not self.installed():
            log.info(f"{self.__class__.__name__} isn't installed, can't deploy")
            return

        self.deployment_actions(env)

    @property
    def commit_hash(self):
        return subprocess.check_output("git rev-parse HEAD", shell=True).decode().strip()
