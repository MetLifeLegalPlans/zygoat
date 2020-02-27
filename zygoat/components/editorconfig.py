from importlib import resources as il_resources

import logging
import os

from zygoat.components import Component
from zygoat.constants import Phases
from . import resources

log = logging.getLogger()
file_name = '.editorconfig'


class EditorConfig(Component):
    def create(self):
        log.info(f'Creating {file_name}')

        with open(file_name, 'w') as f:
            f.write(il_resources.read_text(resources, file_name))

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)

    def delete(self):
        log.warning(f'Deleting {file_name}')
        os.remove(file_name)

    @property
    def installed(self):
        return os.path.exists(file_name)


editorconfig = EditorConfig()
