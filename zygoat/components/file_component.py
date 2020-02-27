from importlib import resources as il_resources

import logging
import os

from zygoat.components import Component
from zygoat.constants import Phases


log = logging.getLogger()


class FileComponent(Component):
    """
    Use this when you want to create a file component that
    tracks the contents of the file that 'filename' points to.
    Note that this file must exist in zygoat's path here:
    'zygoat/components/resources/'.
    """
    def check_setup(f):
        def wrapper(self, *args, **kwargs):
            if not self.filename:
                raise NotImplementedError(
                        'You must specify cls.filename!')
            if not self.resource_pkg:
                raise NotImplementedError(
                        'You must specify cls.resources_pkg!')
            return f(self, *args, **kwargs)
        return wrapper

    @check_setup
    def create(self):
        log.info(f'Creating {self.filename}')

        with open(self.filename, 'w') as f:
            f.write(il_resources.read_text(self.resource_pkg, self.filename))

    @check_setup
    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    @check_setup
    def delete(self):
        log.warning(f'Deleting {self.filename}')
        os.remove(self.filename)

    @check_setup
    @property
    def installed(self):
        return os.path.exists(self.filename)
