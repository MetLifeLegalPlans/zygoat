from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class PrettierRc(FileComponent):
    filename = ".prettierrc"
    resource_pkg = resources
    base_path = Projects.FRONTEND


prettierrc = PrettierRc()
