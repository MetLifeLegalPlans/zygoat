import logging

from zygoat.components import SettingsComponent

from .secret_key import secret_key
from .database_config import database_config
from .debug_config import debug_config
from .installed_apps import installed_apps
from .allowed_hosts import allowed_hosts

log = logging.getLogger()


class Settings(SettingsComponent):
    def create(self):
        red = self.parse()
        first_import_index = red.index(red.find('importnode'))

        log.info('Inserting environ import into django settings')
        red.insert(first_import_index + 1, 'import environ')

        log.info('Inserting environ constructor')
        red.insert(first_import_index + 2, 'env = environ.Env()')

        log.info('Dumping django settings file')
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find('name', value='environ') is not None


settings = Settings(sub_components=[secret_key, database_config, debug_config, installed_apps, allowed_hosts])
