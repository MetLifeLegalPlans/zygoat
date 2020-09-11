import logging

from zygoat.components import SettingsComponent
from redbaron import RedBaron

from .installed_apps import installed_apps

log = logging.getLogger()


class Settings(SettingsComponent):
    def create(self):
        # RedBaron has a *really* obtuse bug where it will not insert end of line comments
        # but it will preserve them in an output dump - so we just insert the raw string here
        lines = self.parse().dumps().split("\n")

        for idx, line in enumerate(lines):
            if "import" in line:
                first_import_index = idx
                break

        log.info("Creating import for zygoat-django settings")
        lines.insert(first_import_index, "from zygoat_django.settings import *  # noqa")

        # We run it through RedBaron again to make sure we've generated valid source code
        red = RedBaron("\n".join(lines))
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()

        return red.find("name", value="zygoat_django") is not None


settings_sub_components = [
    installed_apps,
]

settings = Settings(sub_components=settings_sub_components)
