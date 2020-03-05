from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class NextConfig(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = "next.config.js"
    overwrite = False


next_config = NextConfig()
