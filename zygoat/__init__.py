# Initialize the logger
from . import utils  # noqa

# Disable long tracebacks
import sys

sys.tracebacklimit = 2

__version__ = "0.1.0"
