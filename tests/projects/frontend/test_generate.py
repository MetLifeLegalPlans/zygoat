import pytest

from zygoat.projects.frontend import generate


@pytest.mark.slow
def test_generate_completes(node, temp_dir):
    assert generate(node, temp_dir) is None
