from zygoat.components import Component

from .gitignore import gitignore
from .configuration import configuration


class Cypress(Component):
    pass


cypress = Cypress(sub_components=[configuration, gitignore])
