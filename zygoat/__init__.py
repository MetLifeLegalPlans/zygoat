import os
import sys

import click

from .logging import log
from .projects import backend, frontend, finalize
from .utils import chdir
from . import container_ext

_images = ["python:latest", "node:latest"]

container_ext.patch()


@click.command()
@click.argument("name")
@click.option("--force", "force", flag_value="force", default=False)
def new(name: str, force: bool):
    project_path = os.path.join(os.getcwd(), name)
    if os.path.exists(project_path):
        if not force:
            log.critical(f"Target path {project_path} already exists")
            sys.exit(1)
    else:
        os.mkdir(project_path)

    containers = [container_ext.spawn(image, project_path, wait=True) for image in _images]

    python, node = containers
    with chdir(project_path):
        try:
            backend.generate(python, project_path)
            frontend.generate(node, project_path)
            finalize.generate(project_path)
        finally:
            log.info("Stopping containers...")
            for container in containers:
                # timeout=0 needed because the main process is purposefully hung
                container.stop(timeout=0)
