import boto3
import logging

from click import style

from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run
from zygoat.config import Config
from zygoat.components.base_deployment import BaseDeployment
from zygoat.components.backend.zappa_settings import ZappaSettings


log = logging.getLogger()


class ZappaDeployment(BaseDeployment):
    def is_installed(self, env):
        # TODO make this environment-specific?
        settings = ZappaSettings()
        if not settings.get(env):
            msg = "Zappa settings aren't installed!"
            styled = style(msg, bold=True, fg="red")
            log.error(styled)
            return False
        return True

    def deployment_actions(self, env):
        project_name = self.config.name

        func_name = f"{project_name}-backend-{env}"

        client = boto3.client("lambda")

        log.info("Retrieving current environment configuration")
        environment = client.get_function_configuration(FunctionName=func_name)[
            "Environment"
        ].get("Variables", {})

        log.info("Updating environment configuration")
        environment[f"DJANGO_GIT_COMMIT_HASH"] = self.commit_hash
        environment[f"DJANGO_ENVIRONMENT"] = env

        log.info("Posting environment configuration to the endpoint")
        # TODO "when updating the aws region configuration make sure this takes
        # that into account.
        client.update_function_configuration(
            FunctionName=func_name, Environment={"Variables": environment}
        )

        with use_dir(Projects.BACKEND):
            log.info(f"Deploying {env} with zappa")

            if env not in self.config.deployed_environments:
                # We haven't deployed this app before so we need to use
                # `zappa deploy`.
                cmd = "deploy"
                self.config.deployed_environments.append(env)
                Config.dump(self.config)
            else:
                # We're using the same underlying routes so can just call
                # `zappa update` to update the code running.
                cmd = "update"
            run(["zappa", cmd, env])

            try:
                log.info(f"Running migrations for {self.environment}")
                run(["zappa", "manage", env, "migrate"])
            except Exception:
                log.error("Migrations failed, rolling back deployment")
                run(["zappa", "rollback", env, "-n 1"])

                raise


zappa_deployment = ZappaDeployment()
