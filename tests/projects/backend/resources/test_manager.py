import os

from zygoat.constants import BACKEND

# Copy the manager file itself since it will always exist
# regardless of the generated project structure
_init = "__init__.py"


def test_cp_file(resources):
    assert not os.path.isfile(_init)
    resources.cp(_init)
    assert os.path.isfile(_init)


def test_cp_dir(resources):
    assert not os.path.isdir(BACKEND)
    resources.cp(".", recursive=True)
    assert os.path.isdir(BACKEND)
