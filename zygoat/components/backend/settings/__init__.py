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

log = logging.getLogger()

zygoat_settings_comment = """\"\"\"
This settings file is generated and updated by Zygoat and should not be edited
manually. Instead, update settings via this package's __init__.py.
\"\"\""""


class Settings(SettingsComponent):
    def create(self):
        log.info("Making python package for Django settings")
        os.mkdir(self.settings_directory)

        log.info("Moving the django settings into the settings package")
        os.rename(self.initial_settings_file_path, self.settings_file_path)

        log.info("Creating import for zygoat settings in __init__.py")
        with open(os.path.join(self.settings_directory, "__init__.py"), "a") as f:
            f.write(f"from .{SettingsComponent.MODULE_NAME} import *  # noqa\n")

        red = self.parse()

        log.info("Adding comment to Zygoat settings file")
        red[0].value = zygoat_settings_comment

        first_import_index = red.index(red.find("importnode"))

        log.info("Inserting environ import into django settings")
        red.insert(first_import_index + 1, "import environ")

        log.info("Inserting environ constructor")
        red.insert(first_import_index + 2, "env = environ.Env()")

        log.info("Dumping django settings file")
        self.dump(red)

    @property
    def installed(self):
        return os.path.exists(self.settings_file_path)


settings_sub_components = [
    secret_key,
    database_config,
    debug_config,
    installed_apps,
    allowed_hosts,
    cookies,
    drf_camelize,
    reverse_proxy,
]

settings = Settings(sub_components=settings_sub_components)
