from docker.models.containers import Container
from typing import Union, List, Callable

import os

Command = Union[List[str], str]

# On recent versions of python PathLike includes str
# but we support as far back as 3.9
Path = Union[os.PathLike, str]

Step = Callable[[Container, Path], None]
