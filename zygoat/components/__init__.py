from .base import Component  # noqa
from .settings_component import SettingsComponent  # noqa

from .editorconfig import editorconfig
from .docker_compose import docker_compose
from .backend import backend
from .frontend import frontend

components = [
    editorconfig,
    docker_compose,
    frontend,
    backend,
]
