try:
    import orjson
except ImportError:
    raise ImportError(
        'Orjson is required for this serializer. '
        'Install it with `pip install orjson`.'
    )

from flagzen.serializer import Serializer


class ORJSONSerializer(Serializer):
    def dump(self, flags):
        return orjson.dumps(flags)

    def load(self, dump):
        return orjson.loads(dump)
