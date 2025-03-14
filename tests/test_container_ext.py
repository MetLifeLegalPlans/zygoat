import pytest

from zygoat import container_ext
import tempfile

container_ext.patch()


def test_zg_run_returns_exit_code(python):
    ret_code = python.zg_run("false", throw=False)
    assert ret_code is not None and ret_code == 1
