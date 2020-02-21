from ruamel.yaml import YAML
import logging

from . import __version__


yaml = YAML(typ='safe')
log = logging.getLogger()


class Config:
    def __init__(self, initial_values={}):
        [setattr(self, k, v) for k, v in initial_values.items()]

        if getattr(self, 'version', None) is not None and self.version != __version__:
            log.warning('This project was made with a different version of zygoat. It may be incompatible.')

    @classmethod
    def load_file(cls, file_name):
        # Because YAML is a truly terrible format, as of v1.2 all JSON is *also* YAML
        with open(file_name) as f:
            return cls(initial_values=yaml.load(f.read()))
