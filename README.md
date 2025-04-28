# zygoat

[![Lint and Test](https://github.com/MetLifeLegalPlans/zygoat-gf/actions/workflows/tests.yml/badge.svg)](https://github.com/MetLifeLegalPlans/zygoat-gf/actions/workflows/tests.yml)

<img src="https://user-images.githubusercontent.com/640862/75250233-e287ea80-57a5-11ea-9d9f-553662a17706.jpeg" />

## What is zygoat?

[![Documentation](https://img.shields.io/static/v1?label=&message=Documentation&color=2ea44f)](https://)

`zygoat` is a command line tool used to bootstrap and configure a React/Django/Postgres stack web application.

Its primary goal is to provide a smooth and immediately available developer experience, with production ready tooling set up out of the box.

- Latest stable version of all required libraries
- Preconfigured `docker` images for both local development and production deployment
- Opinionated linters and code formatters are included, along with [GitHub Actions](https://github.com/features/actions) CI workflows
- Full type checking on both the frontend and backend, configured to run quickly and eliminate unnecessary annotations and visual noise
- [pre-commit](https://pre-commit.com/) hooks ready out of the box
- Database, cache, job scheduler, SSR, and more are already configured with helpful defaults and ready to be used
- No configuration necessary - just run `docker compose up --build` and start hacking!

## Installation

```bash
pip install --upgrade git+https://github.com/MetLifeLegalPlans/zygoat
```

## Usage

`zygoat` currently accepts no options but the generated project name.

```bash
zygoat my-cool-app
```

If the target directory (`./my-cool-app` in the above example) already exists, you can pass the `--force` flag to try generating the project inside of it anyways. **This will probably fail if there are already project files in that folder**.

## How does it work?

`zygoat` is structured as a collection of _projects_ that contain a series of self-contained, dynamically resolved _steps_ that modify the generated project. There are currently 3 projects in `zygoat`:

- `zygoat.projects.frontend` - creates + customizes a NextJS frontend
- `zygoat.projects.backend` - creates + customizes a Django backend
- `zygoat.projects.finalize` - adds project-level configuration like `docker-compose.yml`, `Caddyfile`, `.editorconfig`, and so on

Each project (under `zygoat/projects/{name}`) contains a `steps` package. Each `step` is a pure Python file exposing a `run(executor: docker.Container, project_path: os.PathLike)` function. To add a new step, just place a new `.py` file with a `run` function in the `steps` directory for the project.

Here's an example step that installs [Ruff](https://github.com/astral-sh/ruff) as a dev dependency and copies a configuration file for it from the `zygoat.resources` package.

```py
# zygoat/projects/backend/steps/ruff.py
import os

from zygoat.resources import Resources
from zygoat.projects.backend.dependencies import Dependencies

from zygoat.types import Path, Container
from zygoat.logging import log
from zygoat.constants import BACKEND

_path = os.path.join(BACKEND, "ruff.toml")


def run(python: Container, project_path: Path):
    dependencies = Dependencies(python)
    resources = Resources(project_path)

    log.info("Installing ruff")
    dependencies.install("ruff", dev=True)

    log.info(f"Copying {_path}")
    resources.cp(_path)
```

This step will be automatically detected at runtime and executed.

## Further reading

As you can see in the example, there are a number of utilities provided to help make writing writing steps easier. Currently there is only one top-level utility provided, `zygoat.resources.Resources`, which is used to copy files and directories from zygoat to the generated project. Each project also provides its own utilities, which have their own documentation.

Please see the following for more information on each utility (identifiers are links in the [documentation](https://)):

**Global:**

- `zygoat.resources` - Copy files and directories from zygoat to the generated project
- `zygoat.container_ext` - Helper methods exposed on each `docker.Container` object (not typically invoked in steps)

**Backend:**

- `zygoat.projects.backend.dependencies` - Manage Python dependencies in the generated backend
- `zygoat.projects.backend.settings` - Manage Django settings in the generated backend

**Frontend:**

- `zygoat.projects.frontend.dependencies` - Manage JS dependencies in the generated frontend
- `zygoat.projects.frontend.package` - Manage `package.json` in the generated frontend

## How do I test my changes?

Clone the repository and run `poetry install` to fetch dependencies, and then you have two options for testing the project generator:

### Method 1: Pytest

```bash
poetry run pytest -m 'slow or not slow'
```

Runs our test suite, which includes a full run-through of our generated projects as well as individual unit tests for our components.

This is useful for validating changes, but _does not keep_ the generated project after the test suite completes. If you want to do that (for example to inspect the file structure or run the generated project's CI) then you should use the next method.

### Method 2: Direct

```bash
poetry run zygoat my-project-name
```

_or_

```bash
make # Default project name last-run
```

This runs the generator command directly in the same way an end user would and generates `my-project-name` in the current directory. For convenience there is a `Makefile` in the root of the repository that is roughly equivalent to `poetry run zygoat last-run`.

---

## Contributing

`zygoat` is developed using the [Poetry](https://python-poetry.org/docs/) packaging framework for Python projects to make development as simple and portable as possible.
