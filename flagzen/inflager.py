import bisect
import functools
from collections.abc import Iterator, Generator

from flagzen.serializer import Serializer


class State(int):
    def __init__(
        self,
        _value: int | str | bytes | bytearray = 0, /,
        _base: int | None = None,
        inflager: 'Inflager | None' = None,
        **_base_kwd
    ) -> None:
        self._inflager = inflager

    def __new__(
        cls,
        value: int | str | bytes | bytearray = 0, /,
        base: int | None = None,
        inflager: 'Inflager | None' = None
    ):
        if base is None:
            return super().__new__(cls, value)
        return super().__new__(cls, value, base)

    def __iter__(self) -> Iterator[tuple[str, int]]:
        if self._inflager is None:
            yield from ()
        else:
            yield from self._inflager.get(self)


STATE_OVERLOAD_METHODS = (
    '__add__',
    '__sub__',
    '__mul__',
    '__floordiv__',
    '__truediv__',
    '__mod__',
    '__divmod__',
    '__radd__',
    '__rsub__',
    '__rmul__',
    '__rfloordiv__',
    '__rtruediv__',
    '__rmod__',
    '__rdivmod__',
    '__pow__',
    '__pow__',
    '__rpow__',
    '__and__',
    '__or__',
    '__xor__',
    '__lshift__',
    '__rshift__',
    '__rand__',
    '__ror__',
    '__rxor__',
    '__rlshift__',
    '__rrshift__',
    '__neg__',
    '__pos__',
    '__invert__',
    '__trunc__',
    '__ceil__',
    '__floor__',
    '__round__',
    '__eq__',
    '__ne__',
    '__lt__',
    '__le__',
    '__gt__',
    '__ge__',
    '__str__',
    '__float__',
    '__int__',
    '__abs__',
)


def wrapped_method(method):
    def wrapper(self, other):
        return type(self)(method(self, other), inflager=self._inflager)
    return wrapper


for method_name in STATE_OVERLOAD_METHODS:
    setattr(State, method_name, wrapped_method(getattr(int, method_name)))


class Inflager:
    serializer: type[Serializer] = Serializer.default()
    state_class: type[int] = State

    def __init__(self, flags: dict[str, int] | None = None):
        self.flags = flags or {}

    def state(self, value: int = 0) -> State:
        return self.state_class(value, inflager=self)

    def get(self, value: int = 0) -> Generator[tuple[str, int], None, None]:
        # TODO: any faster, please?
        ret = []
        for name, flag in self.flags.items():
            if value & flag:
                bisect.insort(ret, (flag, name))
        yield from map(tuple, map(reversed, ret))

    def register(self, name: str, value: int, overwrite: bool = False) -> None:
        if overwrite:
            self.flags[name] = value
        else:
            self.flags.setdefault(name, value)

    def register_all(self, **mapping: int) -> None:
        self.flags.update(mapping)

    def unregister(self, name: str) -> None:
        self.flags.pop(name, None)

    def unregister_all(self, *names: str) -> None:
        for name in names:
            self.unregister(name)

    def serialize(self) -> bytes:
        return self.serializer.dump(self.flags)

    @classmethod
    def load(cls, dump: bytes, serializer: Serializer | None = None) -> 'Inflager':
        if serializer is None:
            serializer = cls.serializer
        return cls(flags=serializer.load(dump))

    def __repr__(self):
        return f'<{type(self).__name__} {self.flags=!r}>'
