from functools import wraps
import logging

from zygoat.constants import Phases
from zygoat.components import Component
from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

log = logging.getLogger()


class YarnComponent(Component):
    """
    Use this when you want to install a package using yarn.

    :param package: Name of the package to install
    """

    package = None

    def check_setup(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if not self.package:
                raise NotImplementedError("You must specify cls.package!")
            return f(self, *args, **kwargs)

        return wrapper

    @property
    @check_setup
    def installed(self):
        completed_process = run(["yarn", "info", self.package])
        return completed_process.returncode == 0

    @check_setup
    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing {self.package} via yarn")
            run(["yarn", "add", self.package])

    @check_setup
    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)
        with use_dir(Projects.FRONTEND):
            log.info("Upgrading {self.package} via yarn")
            run(["yarn", "upgrade", self.package])

    @check_setup
    def delete(self):
        self.call_phase(Phases.CREATE, force_create=True)
        with use_dir(Projects.FRONTEND):
            log.info("Removing {self.package} via yarn")
            run(["yarn", "remove", self.package])
