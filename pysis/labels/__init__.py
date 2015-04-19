import io
import functools
import warnings
import six

from .decoder import LabelDecoder
from .encoder import LabelEncoder


def load(stream):
    """Parse an isis label from a stream.

    :param stream: a ``.read()``-supporting file-like object containing a label.
        if ``stream`` is a string it will be treated as a filename
    """
    if isinstance(stream, six.string_types):
        with open(stream, 'rb') as fp:
            return LabelDecoder().decode(fp)
    return LabelDecoder().decode(stream)


def loads(data, encoding='utf-8'):
    """Parse an isis label from a string.

    :param data: an isis label as a string

    :returns: a dictionary representation of the given isis label
    """
    if not isinstance(data, bytes):
        data = data.encode(encoding)
    return LabelDecoder().decode(data)


def dump(label, stream):
    LabelEncoder().encode(label, stream)


def dumps(label):
    stream = io.BytesIO()
    LabelEncoder().encode(label, stream)
    return stream.getvalue()


@functools.wraps(load)
def parse_file_label(stream):
    warnings.warn('parse_file_label is deprecated. use load instead.')
    return load(stream)


@functools.wraps(loads)
def parse_label(data, encoding='utf-8'):
    warnings.warn('parse_label is deprecated. use load instead.')
    return loads(data, encoding='utf-8')
