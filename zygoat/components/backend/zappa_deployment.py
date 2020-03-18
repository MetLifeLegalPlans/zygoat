import boto3
import logging
import subprocess
from click import style

from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run
from zygoat.config import Config
from zygoat.components.base_deployment import BaseDeployment
from zygoat.components.backend.zappa_settings import ZappaSettings


log = logging.getLogger()

required_settings = ("domain", "s3_bucket", "aws_region")


def create_lambda_function(project_name):
    log.info(f"Creating lamdba function for {project_name}")
    # TODO fill this in


class ZappaDeployment(BaseDeployment):
    def is_setup(self, env):
        settings = ZappaSettings().get_env_settings(env)
        error_msgs = []
        if not settings:
            error_msgs.append(f"Zappa settings aren't installed for {env}!")
        for name in required_settings:
            if name not in settings:
                error_msgs.append(f"Zappa settings are missing a value for {name}!")
        # Check that we're in a virtual environment.
        if subprocess.check_output('echo "$VIRTUAL_ENV"', shell=True) == b"\n":
            error_msgs.append("Zappa deployment must be run within an active virtualenv!")

        if not error_msgs:
            return True
        for msg in error_msgs:
            styled = style(msg, bold=True, fg="red")
            log.error(styled)
        return False

    def deployment_actions(self, env):
        settings = ZappaSettings().get_env_settings(env)

        project_name = self.config.name

        func_name = f"{project_name}-backend-{env}"

        client = boto3.client("lambda", region_name=settings["aws_region"])

        log.info("Retrieving current environment configuration")
        try:
            environment = client.get_function_configuration(FunctionName=func_name)[
                "Environment"
            ].get("Variables", {})
        except client.exceptions.ResourceNotFoundException:
            create_lambda_function(project_name)
            environment = {}

        log.info("Updating environment configuration")
        environment[f"DJANGO_GIT_COMMIT_HASH"] = self.commit_hash
        environment[f"DJANGO_ENVIRONMENT"] = env

        log.info("Posting environment configuration to the endpoint")
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
