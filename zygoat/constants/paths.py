from os.path import join
from zygoat.constants import WORKSPACE as _w, BACKEND as _b, FRONTEND as _f

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

# Aliases for convenience, to avoid repetition
B = BACKEND
F = FRONTEND
