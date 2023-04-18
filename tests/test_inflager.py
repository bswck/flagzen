def test_state(registry):
    assert list(registry.state(3)) == [('foo', 1), ('bar', 2)]
    assert list(registry.state(1)) == [('foo', 1)]
    assert list(registry.state(2)) == [('bar', 2)]
    assert list(registry.state(0)) == []


def test_register(registry):
    registry.register('baz', 4)
    assert list(registry.state(1 | 2 | 4)) == [('foo', 1), ('bar', 2), ('baz', 4)]
    assert list(registry.state(4)) == [('baz', 4)]


def test_register_overwrite(registry):
    registry.register('foo', 4, overwrite=True)
    assert list(registry.state(2 | 4)) == [('bar', 2), ('foo', 4)]
    assert list(registry.state(4)) == [('foo', 4)]


def test_register_all(registry):
    registry.register_all(baz=4, qux=8)
    assert list(registry.state(1 | 2 | 4 | 8)) == [('foo', 1), ('bar', 2), ('baz', 4), ('qux', 8)]
    assert list(registry.state(4 | 8)) == [('baz', 4), ('qux', 8)]


def test_persist(registry):
    assert registry.load(registry.serialize()).flags == registry.flags
