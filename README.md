# zygoat

[![Lint and Test](https://github.com/MetLifeLegalPlans/zygoat-gf/actions/workflows/tests.yml/badge.svg)](https://github.com/MetLifeLegalPlans/zygoat-gf/actions/workflows/tests.yml)

<img src="https://user-images.githubusercontent.com/640862/75250233-e287ea80-57a5-11ea-9d9f-553662a17706.jpeg" />

## What is zygoat?

`zygoat` is a command line tool used to bootstrap and configure a React/Django/Postgres stack web application.

Linting, test configuration, boilerplate, and development environment are automatically taken care of using `zygoat` so that you can get up and running faster.

## Installation

```bash
pip install --upgrade git+https://github.com/MetLifeLegalPlans/zygoat
```

## Usage

`zygoat` currently accepts no options but the generated project name.

```bash
zygoat my-cool-app
```

## How does it work?

`zygoat` is structured as a collection of _projects_ that contain a series of self-contained, dynamically resolved _steps_ that modify the generated project. There are currently 3 `project`s in `zygoat`:

- `frontend` - creates + customizes a NextJS frontend
- `backend` - created + customizes a Django backend
- `finalize` - adds project-level configuration like `docker-compose.yml`, `Caddyfile`, `.editorconfig`, and so on

Each project (under `zygoat/project/{name}`) contains a `steps` package. To add a new step, place a new `.py` file in the `steps` directory for the project. Here's an example step that installs [Ruff](https://github.com/astral-sh/ruff) as a dev dependency and copies a configuration file for it from our `resources` package.

```py
# zygoat/projects/backend/steps/ruff.py
import os

from zygoat.resources import Resources
from ..dependencies import Dependencies

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

This step will be automatically detected at runtime and executed against the project.

## How do I develop changes for it?

Clone the repository and run `poetry install` to fetch dependencies, and then you have two options for testing the project generator:

### Method 1: Pytest

```bash
poetry run pytest
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

---

## Documentation

TODO
