import pytest

from zygoat.projects.backend import generate


@pytest.mark.slow
def test_generate_completes(python):
    assert generate(python) is None
