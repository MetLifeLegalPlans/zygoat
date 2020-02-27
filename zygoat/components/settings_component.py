import os

from redbaron import RedBaron

from zygoat.utils.files import repository_root
from zygoat.constants import Projects
from . import Component

file_name = 'settings.py'


class SettingsComponent(Component):
    def parse(self):
        with repository_root():
            with open(os.path.join(Projects.BACKEND, Projects.BACKEND, file_name)) as f:
                return RedBaron(f.read())

    def dump(self, data):
        with repository_root():
            with open(os.path.join(Projects.BACKEND, Projects.BACKEND, file_name), 'w') as f:
                f.write(data.dumps())
