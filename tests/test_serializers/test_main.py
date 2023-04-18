import pytest

from flagzen.serializers.blob_serializer import BlobSerializer
from flagzen.serializers.json_serializer import JSONSerializer
from flagzen.serializers.orjson_serializer import ORJSONSerializer


@pytest.fixture(scope='module', params=[BlobSerializer, JSONSerializer, ORJSONSerializer])
def serializer(request):
    yield request.param()


def test_dump(registry, serializer):
    registry.serializer = serializer
    assert serializer.load(serializer.dump(registry.flags)) == registry.flags


def test_serialize(registry, serializer):
    registry.serializer = serializer
    assert registry.load(registry.serialize(), serializer).flags == registry.flags

