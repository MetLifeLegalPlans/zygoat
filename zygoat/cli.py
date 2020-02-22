import click
import logging

log = logging.getLogger()


@click.group()
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    if verbose:
        log.setLevel(logging.DEBUG)


@cli.command()
@click.argument('project_name')
def new(project_name):
    log.debug(f'Attempting creation of {click.style(project_name, bold=True)}')
