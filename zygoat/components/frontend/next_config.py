from zygoat.components import FileComponent, Component
from zygoat.constants import Projects

from . import resources


class NextConfigFile(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = "next.config.js"
    overwrite = False


class ZygoatNextConfigFile(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = "zygoat.next.config.js"
    overwrite = True


class BabelConfigFile(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = ".babelrc"
    overwrite = False


class NextConfig(Component):
    pass


next_config = NextConfig(
    sub_components=[NextConfigFile(), ZygoatNextConfigFile(), BabelConfigFile()]
)
