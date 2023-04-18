class DefaultSerializer:
    def __get__(
        self,
        instance: 'Serializer | None',
        owner: 'type[Serializer] | None' = None
    ) -> 'type[Serializer]':
        try:
            from inflager.serializers.blob_serializer import BlobSerializer as SerializerClass
        except ImportError:
            try:
                from inflager.serializers.orjson_serializer import ORJSONSerializer as SerializerClass
            except ImportError:
                from inflager.serializers.json_serializer import JSONSerializer as SerializerClass
        return SerializerClass


class Serializer:

    def dump(self, flags: dict[str, int]) -> bytes:
        raise NotImplementedError

    def load(self, dump: bytes) -> dict[str, int]:
        raise NotImplementedError

    default = DefaultSerializer()
