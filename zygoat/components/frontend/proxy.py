import os

from zygoat.constants import Projects
from zygoat.components import FileComponent

from . import resources


class Proxy(FileComponent):
    resource_pkg = resources
    filename = "[...slug].js"
    base_path = os.path.join(Projects.FRONTEND, "pages", "api")
    overwrite = False


proxy = Proxy()
