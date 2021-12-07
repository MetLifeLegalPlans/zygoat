import shlex
import subprocess
import os


def run(cmd, *args, **kwargs):
    """
    Takes a shell command split into an array and executes it

    :param cmd: An iterable object with strings inside that form a command
    """
    return subprocess.run(
        " ".join([shlex.quote(c) for c in cmd]),
        *args,
        shell=True,
        check=True,
        **kwargs,
    )


def docker_run(cmd, image, vol, chown=True):
    vol_directory = os.path.join(os.getcwd(), vol)
    prelude = ["docker", "run", "-v", f"{vol_directory}:/data", "-w", "/data", image]
    run(prelude + cmd)

    if chown:
        uid = os.getuid()
        gid = os.getuid()

        run(prelude + ["chown", "-R", f"{uid}:{gid}", "/data"])
