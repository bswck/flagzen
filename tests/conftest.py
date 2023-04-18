import pytest

from flagzen import Registry


@pytest.fixture
def registry():
    return Registry({'foo': 1, 'bar': 2})

