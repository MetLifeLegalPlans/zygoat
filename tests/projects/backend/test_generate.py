import pytest

from zygoat.projects.backend import generate


@pytest.mark.slow
def test_generate_completes(python, temp_dir):
    assert generate(python, temp_dir) is None
