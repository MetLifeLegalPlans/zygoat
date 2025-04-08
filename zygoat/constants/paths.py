from os.path import join

from zygoat.constants import BACKEND as _b
from zygoat.constants import FRONTEND as _f
from zygoat.constants import WORKSPACE as _w

GITIGNORE = ".gitignore"
DOCKERFILE = "Dockerfile"
DOCKERFILE_LOCAL = f"{DOCKERFILE}.local"

dockerfiles = [DOCKERFILE, DOCKERFILE_LOCAL]

WORKSPACE = join("/", _w)
BACKEND = join(WORKSPACE, _b)
FRONTEND = join(WORKSPACE, _f)

# Backend specific
SETTINGS = join(_b, _b, "settings.py")
GUNICORN_CONF = "gunicorn.conf.py"

# Frontend specific
PACKAGE = join(_f, "package.json")
TSCONFIG = join(_f, "tsconfig.json")
PAGES = join(_f, "pages")

# Aliases for convenience, to avoid repetition
B = BACKEND
F = FRONTEND
