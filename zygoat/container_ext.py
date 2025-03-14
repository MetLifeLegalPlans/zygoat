from time import sleep
import os

# Required for 3.9 compatibility
from typing import Any, Optional, Union

import docker

from docker.models.containers import Container

from .constants import paths
from .logging import log
from .errors import CommandError

_client = docker.from_env()


def patch():
    """
    Injects the zg_* suite of helper functions onto Docker's Container model
    """
    _patches = [
        ("zg_run", _zg_run),
        ("zg_run_all", _zg_run_all),
        ("zg_perms", _zg_perms),
    ]

    for name, func in _patches:
        setattr(Container, name, func)


def wait_for(container: Container):
    """
    Waits for a container to enter the running state
    """
    container.reload()
    while container.status != "running":
        log.info(f"Waiting for container {container.image}: {container.status}")
        sleep(0.25)
        container.reload()


def spawn(image: str, project_path: Union[str, os.PathLike], wait: bool = False) -> Container:
    container = _client.containers.run(
        image,
        volumes={project_path: {"bind": paths.WORKSPACE, "mode": "rw"}},
        working_dir=paths.WORKSPACE,
        # Run in the background
        detach=True,
        # Keep the REPL process open so the container stays online
        stdin_open=True,
    )
    if wait:
        wait_for(container)
    return container


def _zg_run(self: Container, *args, correct_perms=True, throw=True, **kwargs) -> int:
    """
    Replacement for exec_run that streams log output in real time
    AND returns the exit code of the command (base exec_run cannot
    do both)

    Adapted from https://gist.github.com/TTimo/f9c9f8521b0006f5c62a12f076ce3d25
    """
    # Get fresh attributes from the server
    self.reload()

    # Create an executable instance to later run
    exec_instance = self.client.api.exec_create(
        self.id,
        *args,
        tty=True,
        environment=self.attrs["Config"]["Env"],
        **kwargs,
    )

    # Start the execution, retrieve generator of output
    exec_output = self.client.api.exec_start(
        exec_instance["Id"],
        tty=True,
        stream=True,
    )

    # Stream output chunks as they become available
    for chunk in exec_output:
        print(chunk.decode(), end="")

    # Retrieve the exit code of the command
    exit_code = self.client.api.exec_inspect(exec_instance["Id"])["ExitCode"]

    # Commands run as root unless otherwise specified, so correct
    # the permissions on the generated project after create
    if correct_perms:
        self.zg_perms()

    if throw and exit_code != 0:
        raise CommandError(f"Command failed: {args} (exit code {exit_code})")

    return exit_code


def _zg_run_all(self: Container, *args, **kwargs) -> Optional[Any]:
    """
    Runs a series of commands in sequence with identical kwargs

    Returns the exit code of the first unsuccessful command,
    or 0 if all commands were successful
    """
    ret_code = None

    for cmd in args:
        ret_code = self.zg_run(cmd, **kwargs)
        if ret_code is not None and ret_code != 0:
            return ret_code

    return ret_code


def _zg_perms(self: Container, *args, **kwargs):
    """
    Corrects file permissions across the whole generated workspace
    """
    uid, gid = [os.getuid(), os.getgid()]
    self.exec_run(f"chown -R {uid}:{gid} {paths.WORKSPACE}")
