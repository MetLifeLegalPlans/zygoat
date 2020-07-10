import logging
import os

from zygoat.components import SettingsComponent

from .secret_key import secret_key
from .database_config import database_config
from .debug_config import debug_config
from .installed_apps import installed_apps
from .allowed_hosts import allowed_hosts
from .cookies import cookies
from .drf_camelize import drf_camelize
from .reverse_proxy import reverse_proxy
from .env import env
from .security import security
from .settings_file import settings_file

log = logging.getLogger()


class Settings(SettingsComponent):
    def create(self):
        log.info("Making python package for Django settings")
        os.makedirs(self.settings_directory, exist_ok=True)

        log.info("Creating import for zygoat settings in __init__.py")
        with open(os.path.join(self.settings_directory, "__init__.py"), "a") as f:
            f.write(f"from .{SettingsComponent.MODULE_NAME} import *  # noqa\n")

    @property
    def installed(self):
        return os.path.exists(self.settings_directory)

    def update(self):
        red = self.parse()
        key_node = red.find("name", value="SECRET_KEY").parent
        log.info("Retrieving existing secret key")
        default_key = key_node.value
        self.existing_secret_key = default_key


settings_sub_components = [
    settings_file,
    secret_key,
    database_config,
    debug_config,
    installed_apps,
    allowed_hosts,
    cookies,
    security,
    drf_camelize,
    reverse_proxy,
    env,
]

settings = Settings(sub_components=settings_sub_components)
