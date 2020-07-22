from zygoat.components import FileComponent
from zygoat.constants import Projects

from . import resources


class JsConfig(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = "jsconfig.json"
    overwrite = False


js_config = JsConfig()
