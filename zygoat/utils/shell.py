import shlex
import subprocess


def run(cmd, *args, **kwargs):
    """
    Takes a shell command split into an array and executes it

    :param cmd: An iterable object with strings inside that form a command
    """
    return subprocess.run(
        " ".join([shlex.quote(c) for c in cmd]), *args, shell=True, check=True, **kwargs,
    )
