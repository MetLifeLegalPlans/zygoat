from .base import Component  # noqa
from .file_component import FileComponent  # noqa
from .settings_component import SettingsComponent  # noqa

from .editorconfig import editorconfig
from .precommit import precommitconfig
from .docker_compose import docker_compose
from .backend import backend
from .frontend import frontend

components = [
    editorconfig,
    precommitconfig,
    docker_compose,
    backend,
    frontend,
]
