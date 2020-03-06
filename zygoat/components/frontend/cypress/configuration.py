import os

from zygoat.constants import Projects
from zygoat.components import FileComponent

from . import resources


class Configuration(FileComponent):
    filename = "cypress.json"
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND)


configuration = Configuration()
