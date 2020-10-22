from zygoat.components import Component, FileComponent
from zygoat.constants import Projects

from .docker_compose import docker_compose
from . import resources


class Dockerfile(Component):
    pass


class Prod(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = "Dockerfile"
    overwrite = False


class Local(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = "Dockerfile.local"
    overwrite = False


dockerfile = Dockerfile(sub_components=[docker_compose, Prod(), Local()])
