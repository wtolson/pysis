# -*- coding: utf-8 -*-

import numpy
from .labels import parse_file_label
from .specialpixels import SPECIAL_PIXELS


class CubeFile(object):
    """ A Isis Cube file reader.

    Attributes:
        filename: The filename if given, otherwise none.
        label: The parsed label header in dictionary form.
        data: A numpy array representing the image data.
        multiplier: A multiplicative factor by which to scale pixel DN.
        base: An additive factor by which to offset pixel DN.
    """

    PIXEL_TYPES = {
        'UnsignedByte': numpy.dtype('uint8'),
        'SignedByte': numpy.dtype('int8'),
        'UnsignedWord': numpy.dtype('uint16'),
        'SignedWord': numpy.dtype('int16'),
        'UnsignedInteger': numpy.dtype('uint32'),
        'SignedInteger': numpy.dtype('int32'),
        'Real': numpy.dtype('float32'),
        'Double': numpy.dtype('float64')
    }

    BYTE_ORDERS = {
        'NoByteOrder': '=',  # system
        'Lsb': '<',          # little-endian
        'Msb': '>'           # big-endian
    }

    SPECIAL_PIXELS = SPECIAL_PIXELS

    @staticmethod
    def open(stream, filename=None):
        """ Open an Isis Cube file.

        Arguments:
            stream: The file name or file object to read as an isis file.
            filename: If stream is a file object, an optional filename to attach
                to the object.

        Returns:
            A new isis cube object from the specified file.
        """
        return CubeFile(stream, filename)

    def apply_scaling(self, copy=True):
        """ Scale pixel values to there true DN.

        Arguments:
            copy: Whether to apply the scalling to a copy of the pixel data
                and leave the orginial unaffected.

        Returns:
            A scalled version of the pixel data.
        """
        if copy:
            return self.multiplier * self.data + self.base

        if self.multiplier != 1:
            self.data *= self.multiplier

        if self.base != 0:
            self.data += self.base

        return self.data

    def apply_numpy_specials(self, copy=True):
        """ Convert isis special pixel values to numpy special pixel values.

                 Isis -> Numpy
                ===============
                 Null ->   nan
                ---------------
                 Lrs  ->  -inf
                 Lis  ->  -inf
                ---------------
                 His  ->   inf
                 Hrs  ->   inf

        Arguments:
            copy: Whether to apply the new special values to a copy of the pixel
                data and leave the orginial unaffected.

        Returns:
            A numpy array with special values converted to numpy's nan, inf and
            -inf.
        """
        if copy:
            data = self.data.astype(numpy.float64)

        elif self.data.dtype != numpy.float64:
            data = self.data = self.data.astype(numpy.float64)

        else:
            data = self.data

        data[data == self.specials['Null']] = numpy.nan
        data[data < self.specials['Min']] = numpy.NINF
        data[data > self.specials['Max']] = numpy.inf

        return data

    def specials_mask(self):
        """ Create a pixel map for special pixels.

        Returns:
            An array where the value is False if the pixel is special and True
            otherwise.
        """
        mask = self.data >= self.specials['Min']
        mask &= self.data <= self.specials['Max']
        return mask

    def get_image_array(self):
        """ Create an array for use in making an image.

        Creates a linear stretch of the image and scales it to between 0 and
        255. Null, Lis and Lrs pixels are set to 0. His and Hrs pixels are set
        to 255.

        Usage:
            from pysis import CubeFile
            from PIL import Image

            # Read in the image and create the image data
            im = CubeFile.open('test.cub')
            data = im.get_image_array()

            # Save the first band to a new file
            Image.fromarray(data[0]).save('test.png')

        Returns:
            A uint8 array of pixel values.
        """
        specials_mask = self.specials_mask()
        data = self.data.copy()

        data[specials_mask] -= data[specials_mask].min()
        data[specials_mask] *= 255 / data[specials_mask].max()

        data[data == self.specials['His']] = 255
        data[data == self.specials['Hrs']] = 255

        return data.astype(numpy.uint8)

    @property
    def bands(self):
        return self.label['IsisCube']['Core']['Dimensions']['Bands']

    @property
    def lines(self):
        return self.label['IsisCube']['Core']['Dimensions']['Lines']

    @property
    def samples(self):
        return self.label['IsisCube']['Core']['Dimensions']['Samples']

    @property
    def tile_lines(self):
        if self.format != 'Tile':
            return None

        return self.label['IsisCube']['Core']['TileLines']

    @property
    def tile_samples(self):
        if self.format != 'Tile':
            return None

        return self.label['IsisCube']['Core']['TileSamples']

    @property
    def format(self):
        return self.label['IsisCube']['Core']['Format']

    @property
    def dtype(self):
        pixels_group = self.label['IsisCube']['Core']['Pixels']
        byte_order = self.BYTE_ORDERS[pixels_group['ByteOrder']]
        pixel_type = self.PIXEL_TYPES[pixels_group['Type']]
        return pixel_type.newbyteorder(byte_order)

    @property
    def specials(self):
        pixel_type = self.label['IsisCube']['Core']['Pixels']['Type']
        return self.SPECIAL_PIXELS[pixel_type]

    @property
    def base(self):
        return self.label['IsisCube']['Core']['Pixels']['Base']

    @property
    def multiplier(self):
        return self.label['IsisCube']['Core']['Pixels']['Multiplier']

    @property
    def start_byte(self):
        return self.label['IsisCube']['Core']['StartByte'] - 1

    @property
    def shape(self):
        return (self.bands, self.lines, self.samples)

    @property
    def size(self):
        return self.bands * self.lines * self.samples

    def __init__(self, stream, filename=None):
        """ Create an Isis Cube file.

        Arguments:
            stream: The file name or file object to read as an isis file.
            filename: If stream is a file object, an optional filename to attach
                to the object.
        """
        if isinstance(stream, basestring):
            self.filename = stream
            with open(self.filename) as f:
                self._open(f)

        else:
            self.filename = filename
            self._open(stream)

    def _open(self, stream):
        self.label = parse_file_label(stream)
        stream.seek(self.start_byte)

        if self.format == 'BandSequential':
            self.data = self._get_bs_data(stream)

        elif self.format == 'Tile':
            self.data = self._get_tile_data(stream)

        else:
            raise Exception('Unkown Isis Cube format (%s)' % self.format)

    def _get_bs_data(self, stream):
        data = numpy.fromfile(stream, self.dtype, self.size)
        return data.reshape(self.shape)

    def _get_tile_data(self, stream):
        tile_lines = self.tile_lines
        tile_samples = self.tile_samples
        tile_size = tile_lines * tile_samples

        lines = xrange(0, self.lines, self.tile_lines)
        samples = xrange(0, self.samples, self.tile_samples)

        dtype = self.dtype
        data = numpy.empty(self.shape, dtype=dtype)

        for band in data:
            for line in lines:
                for sample in samples:
                    sample_end = sample + tile_samples
                    line_end = line + tile_lines
                    chunk = band[line:line_end, sample:sample_end]

                    tile = numpy.fromfile(stream, dtype, tile_size)
                    tile = tile.reshape((tile_lines, tile_samples))

                    chunk_lines, chunk_samples = chunk.shape
                    chunk[:] = tile[:chunk_lines, :chunk_samples]

        return data
