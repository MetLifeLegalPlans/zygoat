from zygoat.components import Component

from .codebuild import codebuild
from .gitignore import gitignore
from .configuration import configuration


class Cypress(Component):
    pass


cypress = Cypress(sub_components=[configuration, gitignore, codebuild])
