from docker.models.containers import Container

from zygoat.constants import paths
from zygoat.logging import log
from zygoat.types import Path
from zygoat.utils import find_steps

from . import steps


def generate(node: Container, project_path: Path) -> None:
    log.info("Starting frontend generation")

    log.info("Updating NPM")
    node.zg_run("npm install -g npm@latest")

    # Collect basic dependencies and generate project
    log.info("Running create-next-app")
    node.zg_run(
        [
            "npx",
            "-y",  # Non-interactively install create-next-app
            "create-next-app@latest",
            "frontend",  # Project name
            "--ts",  # We have to use Typescript for prop type checking
            "--eslint",  # Use Next's default eslint config
            "--app",  # Use React server components
            "--no-tailwind",  # MUI is our design system
            "--no-src-dir",  # An extra src dir is extraneous in our setup
            "--empty",  # Include less Vercel branding in the generated project
            "--yes",  # Take default values for any options we haven't specified
        ]
    )

    # Ready for dynamic step resolution!
    for step in find_steps(steps):
        step(node, project_path)

    # Finally, reformat our project to bring everything back inline
    node.zg_run("npm run format", workdir=paths.F)
