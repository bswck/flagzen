try:
    import construct as cs
except ImportError:
    raise ImportError(
        'Construct is required for this serializer. '
        'Install it with `pip install construct`.'
    )

from flagzen.serializer import Serializer


BLOB = cs.Struct(
    magic=cs.Const(b'INFL'),
    data=cs.PrefixedArray(cs.Int64ul, cs.Sequence(
        cs.CString('utf-8'),
        cs.BytesInteger(64, signed=False),
    )),
)


class BlobSerializer(Serializer):
    blob = BLOB.compile()

    def dump(self, flags):
        return self.blob.build(dict(data=tuple(flags.items())))

    def load(self, dump):
        return dict(self.blob.parse(dump)['data'])
