import click
from importlib import import_module
import logging
import semver

from .components import components
from .config import Config
from .constants import Phases, config_file_name, __version__

log = logging.getLogger()


class ZygoatOutOfDateException(Exception):
    """
    Exception raised when trying to run zygoat on a project initialized with
    a newer version of zygoat.
    """

    def __init__(self, current_version, original_version):
        super().__init__(
            f"Tried to update a zygoat project using a older "
            f"version than the project was created with."
            f"Run with --force if this is intended.\n"
            f"Original version: {original_version}\n"
            f"Current version: {current_version}"
        )


def _is_older_version(version1, version2):
    return semver.compare(version1, version2) < 0


def _call_phase(phase, reverse=False, force=False):
    component_list = [*components]
    config = Config()

    version = config.get("version")
    if _is_older_version(__version__, version):
        log.warn(
            f"Using older version of zygoat than when this package was made. "
            f"Current: {__version__}, Original: {version}."
        )
        if not force:
            raise ZygoatOutOfDateException(__version__, version)

    for extra in config.get("extras", []):
        module, attr = extra.split(":")

        log.info(f"Adding {extra} to the component tree")
        component_list.append(getattr(import_module(module), attr))

    if reverse:
        component_list.reverse()

    for component in component_list:
        component.call_phase(phase)


def _name_project(project_name):
    config = Config()

    if project_name == "" and getattr(config, "name", None) is not None:
        return

    config.name = project_name
    Config.dump(config)


@click.group()
@click.option("--verbose", "-v", is_flag=True)
def cli(verbose):
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


@cli.command(help="Creates a new zygoat settings file and exits")
@click.argument("project_name")
def init(project_name):
    _name_project(project_name)

    log.info(f"Initialized {config_file_name}")
    log.info(str(Config().to_dict()))


@cli.command(help="Creates a new settings file and all components")
@click.option("--force", "-f", is_flag=True)
@click.argument("project_name", default="")
def new(project_name, force):
    log.debug(f"Attempting creation of {click.style(project_name, bold=True)}")

    _name_project(project_name)

    _call_phase(Phases.CREATE, force=force)

    log.info("Done!")
    log.info(
        "Run {} to start your new {} project!".format(
            click.style("docker-compose up --build", fg="cyan", bold=True),
            click.style(project_name, fg="cyan", bold=True),
        )
    )


@cli.command(help="Lists all of the running phase names")
@click.option("--force", "-f", is_flag=True)
def list(force):
    _call_phase(Phases.LIST, force=force)


@cli.command(help="Calls the delete phase on all included build components")
@click.option("--force", "-f", is_flag=True)
def delete(force):
    _call_phase(Phases.DELETE, reverse=True, force=force)

    # remove zygoat settings file
    Config.delete()


@cli.command(help="Calls the update phase on all included build components")
@click.option("--force", "-f", is_flag=True)
def update(force):
    _call_phase(Phases.UPDATE, force=force)


@cli.command(help="Prints the version and exits")
def version():
    log.info(f"Running zygoat v{__version__}")
