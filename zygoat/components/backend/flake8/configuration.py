import os

from zygoat.constants import Projects
from zygoat.components import FileComponent

from . import resources


class Configuration(FileComponent):
    filename = ".flake8"
    resource_pkg = resources
    base_path = os.path.join(Projects.BACKEND)


configuration = Configuration()
