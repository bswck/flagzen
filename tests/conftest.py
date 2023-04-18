import pytest

from flagzen import Inflager


@pytest.fixture
def inflager():
    return Inflager({'foo': 1, 'bar': 2})

