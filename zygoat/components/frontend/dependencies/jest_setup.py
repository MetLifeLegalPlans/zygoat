from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class JestSetup(FileComponent):
    filename = "jest.setup.js"
    resource_pkg = resources
    base_path = Projects.FRONTEND
    overwrite = False


jest_setup = JestSetup()
