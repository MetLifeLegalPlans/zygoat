from .base import Component  # noqa

from .docker_compose import docker_compose
from .backend import backend
from .frontend import frontend

components = [
    docker_compose,
    backend,
    frontend,
]
