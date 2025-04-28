import tempfile

import docker
import pytest

from zygoat import container_ext
from zygoat.utils import chdir


@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()


@pytest.fixture(scope="module")
def temp_dir():
    with tempfile.TemporaryDirectory(dir=".") as path:
        yield path


@pytest.fixture(scope="module")
def python(docker_client: docker.DockerClient, temp_dir):
    container = container_ext.spawn("python:latest", temp_dir, wait=False)
    with chdir(temp_dir):
        yield container
    container.stop(timeout=0)


@pytest.fixture(scope="module")
def node(docker_client: docker.DockerClient, temp_dir):
    container = container_ext.spawn("node:latest", temp_dir, wait=False)
    with chdir(temp_dir):
        yield container
    container.stop(timeout=0)
