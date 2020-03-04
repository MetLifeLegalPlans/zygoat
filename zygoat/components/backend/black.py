from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class Black(FileComponent):
    filename = "pyproject.toml"
    resource_pkg = resources
    base_path = Projects.BACKEND


black = Black()
