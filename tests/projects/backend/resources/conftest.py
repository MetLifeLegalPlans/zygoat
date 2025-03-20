import pytest

from zygoat.resources import Resources
from zygoat.utils import chdir


@pytest.fixture
def resources(temp_dir):
    manager = Resources(temp_dir)
    with chdir(temp_dir):
        yield manager
