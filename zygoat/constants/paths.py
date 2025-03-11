import os
from zygoat.constants import WORKSPACE as _w, BACKEND as _b, FRONTEND as _F

WORKSPACE = os.path.join("/", _w)
BACKEND = os.path.join(WORKSPACE, _b)
FRONTEND = os.path.join(WORKSPACE, _b)

# Aliases for convenience, to avoid repetition
B = BACKEND
F = FRONTEND
