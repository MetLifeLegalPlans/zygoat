import os

from zygoat.components import FileComponent, SettingsComponent
from zygoat.constants import Projects

from . import resources


class SettingsFile(FileComponent):
    filename = "zygoat_settings.py"
    resource_pkg = resources
    base_path = os.path.join(
        Projects.BACKEND, Projects.BACKEND, SettingsComponent.DIRECTORY_NAME,
    )


settings_file = SettingsFile()
