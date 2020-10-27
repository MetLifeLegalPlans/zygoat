from zygoat.components import FileComponent

from . import resources


class PrettierIgnore(FileComponent):
    filename = ".prettierignore"
    resource_pkg = resources


prettierignore = PrettierIgnore()
