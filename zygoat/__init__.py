import os
import sys

import click

from .logging import log
from .projects import backend
from . import container_ext

_images = ["python:latest", "node:latest"]

container_ext.patch()


@click.command()
@click.argument("name")
def new(name: str):
    project_path = os.path.join(os.getcwd(), name)
    if os.path.exists(project_path):
        log.critical(f"Target path {project_path} already exists")
        sys.exit(1)

    containers = [container_ext.spawn(image, project_path, wait=True) for image in _images]

    python, node = containers
    try:
        backend.generate(python=python, node=node)
    finally:
        for container in containers:
            container.stop()
