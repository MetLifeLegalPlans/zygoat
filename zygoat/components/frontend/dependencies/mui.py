import logging
import os

from zygoat.components import Component, FileComponent
from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

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
        with use_dir(Projects.FRONTEND):
            log.info("Installing material-ui core and icons")
            run(["yarn", "add", "@material-ui/core", "@material-ui/icons"])


mui = Mui(sub_components=[App(), Document()])
