import os

from redbaron import RedBaron

from zygoat.utils.files import repository_root
from zygoat.constants import Projects
from . import Component


class SettingsComponent(Component):
    ORIGINAL_FILE_NAME = "settings.py"
    DIRECTORY_NAME = "settings"
    MODULE_NAME = "zygoat_settings"
    FILE_NAME = f"{MODULE_NAME}.py"

    @property
    def initial_settings_file_path(self):
        return os.path.join(
            Projects.BACKEND, Projects.BACKEND, SettingsComponent.ORIGINAL_FILE_NAME
        )

    @property
    def settings_directory(self):
        return os.path.join(
            Projects.BACKEND, Projects.BACKEND, SettingsComponent.DIRECTORY_NAME,
        )

    @property
    def settings_file_path(self):
        return os.path.join(self.settings_directory, SettingsComponent.FILE_NAME,)

    def parse(self):
        with repository_root():
            with open(self.settings_file_path) as f:
                return RedBaron(f.read())

    def dump(self, data):
        with repository_root():
            with open(self.settings_file_path, "w") as f:
                f.write(data.dumps())
