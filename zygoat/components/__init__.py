from .base import Component
from .file_component import FileComponent
from .settings_component import SettingsComponent
from . import resources

from .editorconfig import editorconfig
from .precommit import precommitconfig
from .docker_compose import docker_compose
from .backend import backend
from .frontend import frontend
from .proxy import reverse_proxy

components = [
    editorconfig,
    precommitconfig,
    docker_compose,
    backend,
    frontend,
    reverse_proxy,
]

__all__ = [
    Component,
    FileComponent,
    SettingsComponent,
    components,
    resources,
]
