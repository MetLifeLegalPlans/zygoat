import pytest

from zygoat.utils.dependencies import AbstractDependenciesManager


def test_requires_overrides(python):
    class BadDependencyManager(AbstractDependenciesManager):
        pass

    with pytest.raises(NotImplementedError):
        BadDependencyManager(python)
