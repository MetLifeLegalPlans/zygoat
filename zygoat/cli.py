import click
import logging

from .components import components
from .config import Config
from .constants import Phases, config_file_name

log = logging.getLogger()


@click.group()
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


@cli.command(help='Creates a new zygoat settings file and exits')
def init():
    Config()
    log.info(f'Initialized {config_file_name}')


@cli.command(help='Creates a new settings file and all components')
@click.argument('project_name')
def new(project_name):
    log.debug(f'Attempting creation of {click.style(project_name, bold=True)}')

    config = Config()
    config.name = project_name
    Config.dump(config)

    for component in components:
        component.call_phase(Phases.CREATE)

    log.info('Done!')
    log.info('Run {} to start your new {} project!'.format(
        click.style('docker-compose up --build', fg='cyan', bold=True),
        click.style(project_name, fg='cyan', bold=True),
    ))


@cli.command(help='Lists all of the running phase names')
def list():
    for component in components:
        component.call_phase(Phases.LIST)


@cli.command(help='Calls the delete phase on all included build components')
def delete():
    for component in reversed(components):
        component.call_phase(Phases.DELETE)


@cli.command(help='Calls the update phase on all included build components')
def update():
    for component in components:
        component.call_phase(Phases.UPDATE)
