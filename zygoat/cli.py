import click
import logging
from datetime import datetime

from .components import components
from .config import Config
from .constants import Phases, config_file_name
from .components.backend.zappa_settings import (
    zappa_prompts,
    update_zappa_prompts,
    ZappaSettings,
)

log = logging.getLogger()


def _call_phase(phase, reverse=False, **kwargs):
    component_list = reversed(components) if reverse else components

    for component in component_list:
        component.call_phase(phase, **kwargs)


@click.group()
@click.option("--verbose", "-v", is_flag=True)
def cli(verbose):
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


@cli.command(help="Creates a new zygoat settings file and exits")
def init():
    Config()
    log.info(f"Initialized {config_file_name}")


@cli.command(help="Creates a new settings file and all components")
@click.argument("project_name")
def new(project_name):
    log.debug(f"Attempting creation of {click.style(project_name, bold=True)}")

    config = Config()
    config.name = project_name
    config.deployed_environments = []
    Config.dump(config)

    _call_phase(Phases.CREATE)

    log.info("Done!")
    log.info(
        "Run {} to start your new {} project!".format(
            click.style("docker-compose up --build", fg="cyan", bold=True),
            click.style(project_name, fg="cyan", bold=True),
        )
    )


@cli.command(help="Create components without initializing a new project")
def create():
    _call_phase(Phases.CREATE)


@cli.command(help="Lists all of the running phase names")
def list_phases():
    _call_phase(Phases.LIST)


@cli.command(help="Calls the delete phase on all included build components")
def delete():
    _call_phase(Phases.DELETE, reverse=True)

    # remove zygoat settings file
    Config.delete()


@cli.command(help="Calls the update phase on all included build components")
def update():
    _call_phase(Phases.UPDATE)


@cli.command(help="Deploys all of the included build components")
@click.argument("environment")
def deploy(environment):
    start = datetime.now()
    _call_phase(Phases.DEPLOY, env=environment)
    end = datetime.now()
    minutes, seconds = divmod((end - start).seconds, 60)
    log.info(f"Deployment took {minutes}m {seconds}s")


@cli.command(help="Setup Zappa and allow for deployment")
@click.argument("environment")
def setup_zappa(environment):
    zp = ZappaSettings()
    if click.confirm(
        "You can either create a new settings module or inherit from another. "
        "Would you like to create a new one?"
    ):
        results = _do_zappa_prompts(prompts=zappa_prompts)
    else:
        current = zp.load()
        extends = click.prompt(
            "Which environment would you like to extend from?",
            type=click.Choice(current.keys()),
            show_choices=True,
        )
        inherited = current[extends]
        prompt_data = update_zappa_prompts(inherited)
        results = _do_zappa_prompts(
            results={"extends": extends}, prompts=prompt_data, inherited=inherited
        )

    zp.update(environment, results)


def _do_zappa_prompts(results={}, prompts={}, inherited={}):
    def get_value(default):
        return click.prompt(
            f"Value for {name}",
            default=default,
            confirmation_prompt=True,
            type=(type(default) if default is not None else None),
        )

    for name, default in prompts.items():
        if isinstance(default, dict):
            results[name] = _do_zappa_prompts({}, default)
        elif isinstance(default, list):
            if all(default):
                if not click.confirm(
                    f"Default for {name} is {default}. Do you want to change?"
                ):
                    continue
            new_list = [get_value(None)]
            while click.confirm(f"Do you want to add another entry for {name}?"):
                new_list.append(get_value(None))
            results[name] = new_list
        else:
            results[name] = get_value(default)

    # Now take out all the duplicated ones from the inherited data.
    results = {name: value for name, value in results.items() if value != inherited.get(name)}
    return results
