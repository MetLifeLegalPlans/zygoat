import os

from redbaron import RedBaron

from zygoat.utils.files import repository_root
from zygoat.constants import Projects
from . import Component


class SettingsComponent(Component):
    FILE_NAME = "settings.py"
    DIRECTORY_NAME = "settings"

    @property
    def initial_settings_file_path(self):
        return os.path.join(Projects.BACKEND, Projects.BACKEND, SettingsComponent.FILE_NAME)

    @property
    def settings_directory(self):
        return os.path.join(
            Projects.BACKEND,
            Projects.BACKEND,
            SettingsComponent.DIRECTORY_NAME,
        )

    @property
    def settings_file_path(self):
        # The project leaves it as settings.py
        if os.path.exists(self.initial_settings_file_path):
            return self.initial_settings_file_path

        # The project splits it into a module
        return os.path.join(self.settings_directory, "__init__.py")

    def parse(self):
        with repository_root():
            with open(self.settings_file_path) as f:
                return RedBaron(f.read())

    def dump(self, data):
        with repository_root():
            with open(self.settings_file_path, "w") as f:
                f.write(data.dumps())
