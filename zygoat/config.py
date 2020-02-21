from ruamel.yaml import YAML

from . import __version__
from click import secho, echo


yaml = YAML(typ='safe')


class Config:
    def __init__(self, initial_values={}):
        [setattr(self, k, v) for k, v in initial_values.items()]

        if getattr(self, 'version', None) is not None and self.version != __version__:
            secho('WARNING: ', fg='yellow', bold=True, nl=False)
            echo('This project was made with a different version of zygoat. It may be incompatible.')

    @classmethod
    def from_yaml(cls, file_name):
        # Because YAML is a truly terrible format, as of 1.2 all JSON is *also* YAML
        return cls(initial_values=yaml.load(file_name))
