import pytest
import docker

from zygoat import container_ext
from zygoat.utils import chdir

import tempfile


@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()


@pytest.fixture(scope="module")
def temp_dir():
    with tempfile.TemporaryDirectory() as path:
        yield path


@pytest.fixture(scope="module")
def python(docker_client: docker.DockerClient, temp_dir):
    container = container_ext.spawn("python:latest", temp_dir, wait=False)
    with chdir(temp_dir):
        yield container
    container.stop(timeout=0)
