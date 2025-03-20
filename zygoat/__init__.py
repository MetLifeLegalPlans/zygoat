import os
import sys

import click

from .logging import log
from .projects import backend
from .utils import chdir
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
    os.mkdir(project_path)

    containers = [container_ext.spawn(image, project_path, wait=True) for image in _images]

    python, node = containers
    with chdir(project_path):
        try:
            backend.generate(python, project_path)
        finally:
            log.info("Stopping containers...")
            for container in containers:
                # timeout=0 needed because the main process is purposefully hung
                container.stop(timeout=0)
