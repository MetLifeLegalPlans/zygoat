from docker.models.containers import Container

from zygoat.types import Path
from zygoat.logging import log
from zygoat.utils import find_steps

from . import steps


def generate(node: Container, project_path: Path):
    log.info("Starting frontend generation")

    # Collect basic dependencies and generate project
    log.info("Running create-next-app")
    node.zg_run(
        [
            "npx",
            "-y",  # Non-interactively install create-next-app
            "create-next-app@latest",
            "frontend",  # Project name
            "--js",  # We don't use typescript
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
