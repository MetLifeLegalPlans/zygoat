from docker.models.containers import Container
from zygoat.logging import log
from zygoat.constants import paths


def generate(python: Container = None, node: Container = None):
    log.info("Generating backend")
    cmds = [
        "pip install --upgrade pip",
        "pip install --upgrade django poetry",
        "django-admin startproject backend",
    ]
    for cmd in cmds:
        python.zg_run(cmd)

    python.zg_run("poetry init -n --name backend", workdir=paths.B)
