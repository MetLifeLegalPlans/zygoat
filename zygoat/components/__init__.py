from .base import Component  # noqa

from .backend import backend
from .docker_compose import docker_compose

components = [
    docker_compose,
    backend,
]
