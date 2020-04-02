import logging
import os

from zygoat.components import Component, FileComponent, SettingsComponent
from zygoat.constants import Projects

from . import resources

log = logging.getLogger()

import_path = "backend.proxy.ReverseProxyHandlingMiddleware"


class ProxyFile(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.BACKEND, Projects.BACKEND)
    filename = "proxy.py"
    overwrite = False


class SettingsEntry(SettingsComponent):
    def create(self):
        red = self.parse()
        middleware_list = red.find("name", "MIDDLEWARE").parent.value

        log.info("Adding reverse proxy middleware")
        middleware_list.insert(0, f"'{import_path}'")

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        middleware_list = red.find("name", "MIDDLEWARE").parent.value.to_python()

        return import_path in middleware_list


# Just a shell for hosting the other two components
class ReverseProxy(Component):
    pass


reverse_proxy = ReverseProxy(sub_components=[ProxyFile(), SettingsEntry()])
