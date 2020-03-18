import logging
import subprocess

from zygoat.components.base import Component


log = logging.getLogger()


class BaseDeployment(Component):
    def deployment_actions(self, env):
        raise NotImplementedError

    @property
    def installed(self):
        # Because we need to know the environment before determining whether we can
        # deploy, assume this is installed and then check in `deploy`.
        return True

    def deploy(self, env="staging", **kwargs):
        if not self.is_setup(env):
            return

        self.deployment_actions(env, **kwargs)

    @property
    def commit_hash(self):
        return subprocess.check_output("git rev-parse HEAD", shell=True).decode().strip()
