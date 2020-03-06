from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class Eslintrc(FileComponent):
    filename = ".eslintrc.js"
    resource_pkg = resources
    base_path = Projects.FRONTEND


eslintrc = Eslintrc()
