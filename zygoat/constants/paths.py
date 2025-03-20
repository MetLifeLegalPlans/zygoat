from os.path import join
from zygoat.constants import WORKSPACE as _w, BACKEND as _b, FRONTEND as _f

WORKSPACE = join("/", _w)
BACKEND = join(WORKSPACE, _b)
FRONTEND = join(WORKSPACE, _f)

# Backend specific
SETTINGS = join(_b, _b, "settings.py")

# Frontend specific
PACKAGE = join(_f, "package.json")

# Aliases for convenience, to avoid repetition
B = BACKEND
F = FRONTEND
