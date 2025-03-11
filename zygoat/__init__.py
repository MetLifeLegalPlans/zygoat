import os
import sys
from time import sleep

import click
import docker
from docker.models.containers import Container

from .logging import log
from .projects import backend
from .constants import paths

docker_client = docker.from_env()

_images = ["python:latest", "node:latest"]


def _zg_run(self, *args, **kwargs):
    ret_code, output = self.exec_run(*args, stream=True, tty=True, **kwargs)
    for chunk in output:
        print(chunk.decode())
    return ret_code


Container.zg_run = _zg_run


@click.command()
@click.argument("name")
def new(name: str):
    project_path = os.path.join(os.getcwd(), name)
    if os.path.exists(project_path):
        log.critical(f"Target path {project_path} already exists")
        sys.exit(1)

    containers = [
        docker_client.containers.run(
            image,
            volumes={project_path: {"bind": paths.WORKSPACE, "mode": "rw"}},
            working_dir=paths.WORKSPACE,
            detach=True,
            # Keep the container running
            stdin_open=True,
        )
        for image in _images
    ]

    for container in containers:
        # Oftentimes the delay of submitting both containers is enough
        # for at least one of them to start, so skip a useless log
        container.reload()
        while container.status != "running":
            log.info(f"Waiting for container {container.image}: {container.status}")
            sleep(1)
            container.reload()

    python, node = containers
    try:
        backend.generate(python=python, node=node)
    finally:
        for container in containers:
            container.exec_run(f"chown -R 1000:1000 {paths.WORKSPACE}")
            container.stop()
