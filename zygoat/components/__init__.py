from .base import Component
from .file_component import FileComponent
from .settings_component import SettingsComponent
from . import resources

from .editorconfig import editorconfig
from .codebuild import codebuild
from .script import cistart
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
    codebuild,
    cistart,
]

__all__ = [
    Component,
    FileComponent,
    SettingsComponent,
    components,
    resources,
]
