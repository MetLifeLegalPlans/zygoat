from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class JestConfig(FileComponent):
    filename = "jest.config.js"
    resource_pkg = resources
    base_path = Projects.FRONTEND
    overwrite = False


jest_config = JestConfig()
