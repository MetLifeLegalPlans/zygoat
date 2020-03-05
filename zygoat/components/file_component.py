from functools import wraps
from importlib import resources as il_resources
import logging
import os

from zygoat.components import Component
from zygoat.constants import Phases
from zygoat.components import resources


log = logging.getLogger()


class FileComponent(Component):
    """
    Use this when you want to create a file component that
    tracks the contents of the file that 'filename' points to.
    Note that this file must exist in zygoat's path here:
    'zygoat/components/resources/'.
    """

    resource_pkg = resources
    base_path = "./"
    overwrite = True

    def check_setup(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if not self.filename:
                raise NotImplementedError("You must specify cls.filename!")
            return f(self, *args, **kwargs)

        return wrapper

    @check_setup
    def create(self):
        log.info(f"Creating {self.path}")
        os.makedirs(self.base_path, exist_ok=True)
        with open(self.path, "w") as f:
            f.write(il_resources.read_text(self.resource_pkg, self.filename))

    @check_setup
    def update(self):
        self.call_phase(Phases.CREATE, force_create=self.overwrite)

    @check_setup
    def delete(self):
        log.warning(f"Deleting {self.path}")
        os.remove(self.path)
        try:
            os.rmdir(self.base_path)
            log.warning(f"Deleting {self.base_path}")
        except OSError:
            log.warning(f"Skipping {self.base_path}")

    @property
    @check_setup
    def installed(self):
        return os.path.exists(self.path)

    @property
    def path(self):
        return os.path.join(self.base_path, self.filename)
