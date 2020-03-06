import os

from zygoat.constants import Projects
from zygoat.components import FileComponent

from . import resources


class Gitignore(FileComponent):
    filename = ".gitignore"
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND, "cypress")


gitignore = Gitignore()
