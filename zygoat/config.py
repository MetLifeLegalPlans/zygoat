from contextlib import contextmanager
import os
import sys

from box import Box
from click import style
from ruamel.yaml import YAML
import logging

from . import __version__
from .utils.files import find_nearest
from .constants import config_file_name


yaml = YAML(typ="safe")
yaml.default_flow_style = False
log = logging.getLogger()


class Config(object):
    def __new__(self, initial_data={}):
        """
        Allows us to create a new Config instance that loads itself and returns a box

        :param initial_data: When creating a new config file, add this to the file
        """
        try:
            return Config.load()
        except FileNotFoundError:
            log.debug("Config file not found, creating a new one")

        try:
            repo_root = os.path.dirname(find_nearest(".git"))

            with open(os.path.join(repo_root, config_file_name), "w"):
                pass
        except FileNotFoundError:
            log.critical("Zygoat must be run inside a git repository")
            log.critical(
                "Run "
                + style("git init", fg="green", bold=True)
                + " to initialize a git repository"
            )
            sys.exit(1)

        data = {"version": __version__}
        data.update(initial_data)

        Config.dump(Box(data))

        return Config.load()

    @classmethod
    @contextmanager
    def settings_file(cls, mode="r"):
        f = open(find_nearest(config_file_name), mode)

        try:
            yield f
        finally:
            f.close()

    @classmethod
    def load(cls):
        with cls.settings_file() as f:
            return Box(yaml.load(f.read()))

    @classmethod
    def dump(cls, data):
        with cls.settings_file(mode="w") as f:
            yaml.dump(data.to_dict(), f)

    @classmethod
    def delete(cls):
        os.remove(find_nearest(config_file_name))
