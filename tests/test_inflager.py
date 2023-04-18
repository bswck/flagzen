def test_state(inflager):
    assert list(inflager.state(3)) == [('foo', 1), ('bar', 2)]
    assert list(inflager.state(1)) == [('foo', 1)]
    assert list(inflager.state(2)) == [('bar', 2)]
    assert list(inflager.state(0)) == []


def test_register(inflager):
    inflager.register('baz', 4)
    assert list(inflager.state(1 | 2 | 4)) == [('foo', 1), ('bar', 2), ('baz', 4)]
    assert list(inflager.state(4)) == [('baz', 4)]


def test_register_overwrite(inflager):
    inflager.register('foo', 4, overwrite=True)
    assert list(inflager.state(2 | 4)) == [('bar', 2), ('foo', 4)]
    assert list(inflager.state(4)) == [('foo', 4)]


def test_register_all(inflager):
    inflager.register_all(baz=4, qux=8)
    assert list(inflager.state(1 | 2 | 4 | 8)) == [('foo', 1), ('bar', 2), ('baz', 4), ('qux', 8)]
    assert list(inflager.state(4 | 8)) == [('baz', 4), ('qux', 8)]


def test_persist(inflager):
    assert inflager.load(inflager.serialize()).flags == inflager.flags
