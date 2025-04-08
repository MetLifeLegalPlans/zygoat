import os
from typing import Callable, List, Union

from docker.models.containers import Container

# On recent versions of python PathLike includes str
# but we support as far back as 3.9
Path = Union[os.PathLike, str]

Command = Union[List[str], str]
Step = Callable[[Container, Path], None]
