import boto3
import logging

from click import style

from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run
from zygoat.config import Config
from zygoat.components.base_deployment import BaseDeployment
from zygoat.components.backend.zappa_settings import ZappaSettings


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class BackendDeployment(BaseDeployment):
    def installed(self):
        settings = ZappaSettings()
        if not settings.installed:
            msg = "Zappa settings aren't installed!"
            styled = style(msg, bold=True, fg="red")
            log.error(styled)
            return False
        return True

    def deployment_actions(self, env):
        func_name = f"backend-{env}"

        config = Config()
        project_name = config.name

        client = boto3.client("lambda")

        log.info("Retrieving current environment configuration")
        environment = client.get_function_configuration(FunctionName=func_name)[
            "Environment"
        ].get("variables", {})

        log.info("Updating environment configuration")
        environment[f"{project_name}_GIT_COMMIT_HASH"] = self.commit_hash
        environment[f"{project_name}_ENVIRONMENT"] = env

        log.info("Posting environment configuration to the endpoint")
        client.update_function_configuration(
            FunctionName=func_name, Environment={"Variables": environment}
        )

        with use_dir(Projects.BACKEND):
            log.info(f"Deploying {env} with zappa")

            if not config.has_deployed:
                # We haven't deployed this app before so we need to use
                # `zappa deploy`.
                cmd = "deploy"
                config.has_deployed = True
                Config.dump(config)
            else:
                # We're using the same underlying routes so can just call
                # `zappa update` to update the code running.
                cmd = "update"
            run(f"zappa {cmd} {env}")

            try:
                log.info(f"Running migrations for {self.environment}")
                run(f"zappa manage {env} migrate")
            except Exception:
                log.error("Migrations failed, rolling back deployment")
                run(f"zappa rollback {env} -n 1")

                raise


backend_deployment = BackendDeployment()
