import pytest

from zygoat import container_ext
from zygoat.errors import CommandError

container_ext.patch()


def test_zg_run_returns_exit_code(python):
    ret_code = python.zg_run("false", throw=False)
    assert ret_code is not None and ret_code == 1


def test_zg_run_throws(python):
    with pytest.raises(CommandError):
        python.zg_run("false")
