import click
from importlib import import_module
import logging

from .components import components
from .config import Config
from .constants import Phases, config_file_name, __version__

log = logging.getLogger()


def _call_phase(phase, reverse=False):
    component_list = reversed(components) if reverse else [*components]
    config = Config()

    for extra in config.get("extras", []):
        module, attr = extra.split(":")

        log.info(f"Adding {extra} to the component tree")
        component_list.append(getattr(import_module(module), attr))

    for component in component_list:
        component.call_phase(phase)


def _name_project(project_name):
    config = Config()
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


@cli.command(help="Creates a new settings file and all components")
@click.argument("project_name")
def new(project_name):
    log.debug(f"Attempting creation of {click.style(project_name, bold=True)}")

    _name_project(project_name)

    _call_phase(Phases.CREATE)

    log.info("Done!")
    log.info(
        "Run {} to start your new {} project!".format(
            click.style("docker-compose up --build", fg="cyan", bold=True),
            click.style(project_name, fg="cyan", bold=True),
        )
    )


@cli.command(help="Lists all of the running phase names")
def list():
    _call_phase(Phases.LIST)


@cli.command(help="Calls the delete phase on all included build components")
def delete():
    _call_phase(Phases.DELETE, reverse=True)

    # remove zygoat settings file
    Config.delete()


@cli.command(help="Calls the update phase on all included build components")
def update():
    _call_phase(Phases.UPDATE)


@cli.command(help="Prints the version and exits")
def version():
    log.info(f"Running zygoat v{__version__}")
