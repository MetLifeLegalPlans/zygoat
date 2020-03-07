import os
import json
import logging

from zygoat.config import Config
from zygoat.constants import deploy_options, production
from zygoat.components.file_component import FileComponent


log = logging.getLogger()


class ZappaSettings(FileComponent):
    filename = "zappa_settings.json"
    base_path = "backend/"

    def create(self):
        config = Config()
        try:
            domain_name = config.domain_name
        except KeyError:
            log.error("Can't initialize zappa settings file without a domain name!")
            return

        log.info(f"Creating {self.path}")
        os.makedirs(self.base_path, exist_ok=True)

        contents = {
            "base": {
                "aws_region": "us-east-1",
                "apigateway_policy": "allow-from-vpn.json",
                "django_settings": "backend.settings",
                "profile_name": "default",
                "project_name": "backend",
                "runtime": "python3.7",
                "s3_bucket": "com.willing.zappa-staging-deployments",
                "slim_handler": True,
                "vpc_config": {
                    "subnets": ["subnet-0bd3002fa3d21142f", "subnet-06f38c8eef613bc98"],
                    "securityGroupIds": ["sg-027c6d8ae04414868"],
                },
                "timeout_seconds": 900,
                "certificate_arn": "arn:aws:acm:us-east-1:818831340115:certificate/72bec828-02c1-4d2d-9e4d-69868e0119d9",
            }
        }

        for name in deploy_options:
            contents[name] = {
                "extends": "base",
                "domain": f"{name}.{domain_name}.com",
            }
        # Add in production-specific stuff.
        contents[production]["vpc_config"] = {
            "SubnetIds": ["subnet-0bd3002fa3d21142f", "subnet-06f38c8eef613bc98"],
            "SecurityGroupIds": ["sg-032c7fb83a9d44dbd"],
        }
        contents[production]["apigateway_policy"] = ("allow-from-anywhere.json",)
        contents[production]["s3_bucket"] = (f"com.{domain_name}.zappa-prod-deployments",)
        contents[production]["domain"] = f"app.{domain_name}.com"

        with open(self.path, "w") as f:
            json.dump(contents, f, indent=2)


zappa_settings = ZappaSettings()
