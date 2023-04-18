import pytest

from inflager.serializers.blob_serializer import BlobSerializer
from inflager.serializers.json_serializer import JSONSerializer
from inflager.serializers.orjson_serializer import ORJSONSerializer


@pytest.fixture(scope='module', params=[BlobSerializer, JSONSerializer, ORJSONSerializer])
def serializer(request):
    yield request.param()


def test_dump(inflager, serializer):
    inflager.serializer = serializer
    assert serializer.load(serializer.dump(inflager.flags)) == inflager.flags


def test_serialize(inflager, serializer):
    inflager.serializer = serializer
    assert inflager.load(inflager.serialize(), serializer).flags == inflager.flags

