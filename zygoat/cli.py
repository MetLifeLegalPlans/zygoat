import click

from .config import Config


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file_name')
def load(file_name):
    Config.load_file(file_name)
