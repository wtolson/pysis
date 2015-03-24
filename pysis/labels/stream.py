import io


class StreamBase(object):
    pass


class BufferedStream(StreamBase):
    def __init__(self, raw):
        """Create a new buffered reader using the given readable raw IO object.
        """
        self.raw = raw
        self.buffer_size = io.DEFAULT_BUFFER_SIZE
        self._read_buf = b''
        self._read_pos = 0

    def read(self, n):
        """Read n bytes.
        Returns exactly n bytes of data unless the underlying raw IO
        stream reaches EOF.
        """
        buf = self._read_buf
        pos = self._read_pos
        end = pos + n

        if end <= len(buf):
            # Fast path: the data to read is fully buffered.
            self._read_pos += n
            return buf[pos:end]

        # Slow path: read from the stream until enough bytes are read,
        # or until an EOF occurs or until read() would block.
        wanted = max(self.buffer_size, n)
        while len(buf) < end:
            chunk = self.raw.read(wanted)
            if not chunk:
                break
            buf += chunk

        self._read_buf = buf[end:]  # Save the extra data in the buffer.
        self._read_pos = 0
        return buf[pos:end]

    def peek(self, n):
        """Returns buffered bytes without advancing the position.
        The argument indicates a desired minimal number of bytes; we
        do at most one raw read to satisfy it.  We never return more
        than self.buffer_size.
        """
        buf = self._read_buf
        pos = self._read_pos
        end = pos + n

        if end <= len(buf):
            # Fast path: the data to read is fully buffered.
            return buf[pos:end]

        # Slow path: read from the stream until enough bytes are read,
        # or until an EOF occurs or until read() would block.
        wanted = max(self.buffer_size, n)
        while len(buf) < end:
            chunk = self.raw.read(wanted)
            if not chunk:
                break
            buf += chunk

        self._read_buf = buf
        return buf[pos:end]


class ByteStream(StreamBase):
    def __init__(self, raw):
        """Create a new buffered reader using the given byte array.
        """
        self.raw = raw
        self._read_pos = 0

    def read(self, n):
        """Read n bytes.
        Returns exactly n bytes of data unless the underlying raw IO
        stream reaches EOF.
        """
        pos = self._read_pos
        self._read_pos = min(len(self.raw), pos + n)
        return self.raw[pos:self._read_pos]

    def peek(self, n):
        """Returns buffered bytes without advancing the position.
        The argument indicates a desired minimal number of bytes; we
        do at most one raw read to satisfy it.  We never return more
        than self.buffer_size.
        """
        pos = self._read_pos
        end = pos + n
        return self.raw[pos:end]
