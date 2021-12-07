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


def docker_run(cmd, image, vol, chown=True, *args, **kwargs):
    vol_directory = os.path.join(os.getcwd(), vol)
    prelude = ["docker", "run", "-v", f"{vol_directory}:/data", "-w", "/data", image]
    ret = run(prelude + cmd, *args, **kwargs)

    if chown:
        uid = os.getuid()
        gid = os.getuid()

        run(prelude + ["chown", "-R", f"{uid}:{gid}", "/data"])

    return ret


def multi_docker_run(cmds, *args, **kwargs):
    cmd = "".join([shlex.join(c) + ";" for c in cmds])
    print(cmd)
    return docker_run(["/bin/bash", "-c", cmd], *args, **kwargs)
