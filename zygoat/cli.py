import click
import logging

from .config import Config
from . import __version__

log = logging.getLogger()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name')
def new(project_name):
    log.info('Testing!')
