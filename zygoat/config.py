import os

from box import Box
from ruamel.yaml import YAML
import logging

from . import __version__
from .utils.files import find_nearest


yaml = YAML(typ='safe')
yaml.default_flow_style = False
log = logging.getLogger()


class Config:
    def __init__(self):
        pass

    @classmethod
    def load(cls):
        """
        Locates the nearest zygoat_settings.yaml file and loads it
        """
        with open(find_nearest('zygoat_settings.yaml')) as f:
            return Box(yaml.load(f.read()))
