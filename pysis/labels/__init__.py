import io
from .parser import LabelParser


def get_label(stream, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """Extract the label string from an isis file.

    :param stream: ff stream is a string it will be treated as a filename
        otherwise it will be treated as if it were a file object

    :param buffer_size: the chunksize to read the label in by

    :returns: the label of the isis file as a string
    """
    if isinstance(stream, basestring):
        with open(stream, 'rb') as fp:
            return get_label(fp)

    label = b''

    while 1:
        data = stream.read(buffer_size)
        if not data:
            break

        label_end = data.find('\0')
        if label_end == -1:
            label += data
            continue

        label += data[:label_end]

    return label


def parse_label(label):
    """Parse an isis label from a string.

    :param label: an isis label as a string

    :returns: a dictionary representation of the given isis label
    """
    return LabelParser().parse(label)


def parse_file_label(stream):
    """Parse an isis label from a stream.

    :param stream: if stream is a string it will be treated as a filename
        otherwise it will be treated as if it were a file object

    :returns: a dictionary representation of the given isis label.
    """
    if isinstance(stream, basestring):
        with open(stream, 'rb') as fp:
            return LabelParser().parse(fp)
    return LabelParser().parse(stream)
