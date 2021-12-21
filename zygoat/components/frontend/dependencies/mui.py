import logging
import os

from zygoat.components import Component, FileComponent
from zygoat.constants import Projects, Images
from zygoat.utils.shell import docker_run

from . import resources

log = logging.getLogger()


class MuiFile(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND, "pages")
    overwrite = False


class App(MuiFile):
    filename = "_app.js"


class Document(MuiFile):
    filename = "_document.js"


class Mui(Component):
    def create(self):
        log.info("Installing material-ui core and icons")
        docker_run(
            [
                "yarn",
                "add",
                "@mui/material",
                "@mui/icons-material",
                "@emotion/cache",
                "@emotion/react",
                "@emotion/server",
                "@emotion/styled",
            ],
            Images.NODE,
            Projects.FRONTEND,
        )


mui = Mui(sub_components=[App(), Document()])
