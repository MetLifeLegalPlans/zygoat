import click
import logging

from .components import backend
from .config import Config

log = logging.getLogger()


@click.group()
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    if verbose:
        log.setLevel(logging.DEBUG)

    Config()


@cli.command()
def init():
    # Handled by the CLI constructor creating a new Config object
    log.info('Initialized zygoat_settings.yaml')


@cli.command()
@click.argument('project_name')
def new(project_name):
    log.debug(f'Attempting creation of {click.style(project_name, bold=True)}')

    config = Config()
    config.name = project_name
    Config.dump(config)

    backend.call_phase('create')
