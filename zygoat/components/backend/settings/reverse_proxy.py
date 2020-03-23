import logging
import os

from zygoat.components import Component, FileComponent, SettingsComponent
from zygoat.constants import Projects

from . import resources

log = logging.getLogger()


class ProxyFile(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.BACKEND, Projects.BACKEND)
    filename = "proxy.py"


class SettingsEntry(SettingsComponent):
    def create(self):
        red = self.parse()
        middleware_list = red.find("name", "MIDDLEWARE").parent.value

        log.info("Adding reverse proxy middleware")
        middleware_list.insert(0, "'backend.proxy.ReverseProxyHandlingMiddleware'")

        self.dump(red)


# Just a shell for hosting the other two components
class ReverseProxy(Component):
    pass


reverse_proxy = ReverseProxy(sub_components=[ProxyFile(), SettingsEntry()])
