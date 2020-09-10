import logging

from zygoat.components import SettingsComponent

from .installed_apps import installed_apps

log = logging.getLogger()


class Settings(SettingsComponent):
    def create(self):
        red = self.parse()

        first_import_index = red.index(red.find("importnode"))

        log.info("Creating import for zygoat-django settings in __init__.py")
        red.insert(first_import_index + 1, "from zygoat_django.settings import *")

    @property
    def installed(self):
        red = self.parse()

        return red.find("name", value="zygoat_django") is not None


settings_sub_components = [
    installed_apps,
]

settings = Settings(sub_components=settings_sub_components)
