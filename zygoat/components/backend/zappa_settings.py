import copy
import json
import logging

from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run


log = logging.getLogger()

zappa_prompts = {
    "aws_region": "us-east-1",
    "apigateway_policy": "allow-from-anywhere.json",
    "django_settings": "backend.settings",
    "profile_name": "default",
    "project_name": "backend",
    "runtime": "python3.7",
    "slim_handler": False,
    "s3_bucket": None,
    "timeout_seconds": 30,
    "certificate_arn": None,
    "domain": None,
    "vpc_config": {"SubnetIds": [None], "SecurityGroupIds": [None],},
}


def update_zappa_prompts(updates):
    prompts = copy.deepcopy(zappa_prompts)
    prompts.update(updates)
    return prompts


class ZappaSettings:
    filename = "zappa_settings.json"

    def update(self, env, updates):
        current = self.load()
        current[env] = updates
        self.dump(current)

        # Now certify the domain with the certificate manager.
        print("Certifying the domain with the certificate manager...")
        run(["zappa", "certify", env])

    def dump(self, data):
        with use_dir(Projects.BACKEND):
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=2)

    def load(self):
        with use_dir(Projects.BACKEND):
            try:
                with open(self.filename) as f:
                    return json.load(f)
            except FileNotFoundError:
                return {}
