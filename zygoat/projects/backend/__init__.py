from docker.models.containers import Container
from zygoat.logging import log
from zygoat.constants import paths


def generate(python: Container = None, node: Container = None):
    log.info("Generating backend")
    python.zg_run_all(
        "pip install --upgrade pip",
        "pip install --upgrade django poetry",
        "django-admin startproject backend",
    )

    python.zg_run("poetry init -n --name backend", workdir=paths.B)
