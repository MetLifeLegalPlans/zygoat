from .shell import multi_docker_run
from .files import repository_root
from zygoat.constants import Projects, ConfigDefaults
from zygoat.config import Config


def install_dependencies(*args, dev=False):
    """
    Installs/upgrades Python dependencies for the backend, and places them in
    the appropriate production or dev requirements files.

    :param args: The packages to install
    :type args: str
    :param dev: Specifies if this is a development or production dependency
    :type dev: bool, optional
    """

    try:
        image = Config().images.PYTHON
    except AttributeError:
        image = ConfigDefaults.images.PYTHON

    with repository_root():
        add_command = ["poetry", "add"]
        if dev:
            add_command.append("--dev")

        multi_docker_run(
            [
                [
                    "pip",
                    "install",
                    "--upgrade",
                    "pip",
                    "poetry",
                ],
                add_command + list(args),  # args is a tuple and those can't be concatenated
            ],
            image,
            Projects.BACKEND,
        )
