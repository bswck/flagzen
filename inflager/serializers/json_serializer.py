import json

from inflager.serializer import Serializer


class JSONSerializer(Serializer):
    def dump(self, flags, encoding: str = 'utf-8'):
        return json.dumps(flags).encode(encoding)

    def load(self, dump):
        return json.loads(dump)
