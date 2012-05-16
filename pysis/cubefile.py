# -*- coding: utf-8 -*-
#
#   cubefile.py
#   Copyright 2011 William Trevor Olson <trevor@heytrevor.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
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
        'UnsignedByte': np.dtype('uint8'),
        'SignedByte': np.dtype('int8'),
        'UnsignedWord': np.dtype('uint16'),
        'SignedWord': np.dtype('int16'),
        'UnsignedInteger': np.dtype('uint32'),
        'SignedInteger': np.dtype('int32'),
        'Real': np.dtype('float32'),
        'Double': np.dtype('float64')
    }

    BYTE_ORDERS = {
        'NoByteOrder': '=',
        'Lsb': '<', # little-endian
        'Msb': '>' # big-endian
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
        if isinstance(stream, basestring):
            with open(stream) as f:
                return CubeFile()._open(f, stream)

        return CubeFile()._open(stream, filename)

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

    def specials_mask(self):
        """ Create a pixel map for special pixels.

        Returns:
            An array where the value is False if the pixel is special and True
            otherwise.
        """
        mask  = self.data >= self.specials['Min']
        mask &= self.data <= self.specials['Max']
        return mask

    def get_image_array(self):
        """ Create an array for use in making an image.

        Creates a linear stretch of the image and scales it to between 0 and
        255. Null, Lis and Lrs pixels are set to 0. His and Hrs pixels are set
        to 255.

        Usage:
            from pysis import CubeFile
            from PIL import image

            # Read in the image and create the image data
            im = CubeFile.open('test.cub')
            data = im.get_image_array()

            # Save the first band to a new file
            Image.fromarray(data[0]).save('test.png')

        Returns:
            A uint8 array of pixel values.
        """
        specials_mask = self.specials_mask()
        data          = self.data.copy()

        data[specials_mask] -= data[specials_mask].min()
        data[specials_mask] *= 255 / data[specials_mask].max()

        data[data == self.specials['His']] = 255
        data[data == self.specials['Hrs']] = 255

        return data.astype(np.uint8)

    def _open(self, stream, filename):
        self.filename = filename
        self.label    = parse_file_label(stream)

        (self.bands, self.lines, self.samples)   = self._get_dims()
        (self.dtype, self.specials, self.base, self.multiplier) = self._get_pixel_info()

        start = self._get_data_start()
        stream.seek(start)

        self.format = self.label['IsisCube']['Core']['Format']
        if self.format == 'BandSequential':
            self.data = self._read_bs_data(stream)

        elif self.format == 'Tile':
            self.data = self._read_tile_data(stream)

        else:
            raise Excption('Unkown Isis Cube format (%s)' % self.format)

        return self

    def _get_dims(self):
        dims = self.label['IsisCube']['Core']['Dimensions']
        return dims['Bands'], dims['Lines'], dims['Samples']

    def _get_pixel_info(self):
        pixels_group = self.label['IsisCube']['Core']['Pixels']

        byte_order   = self.BYTE_ORDERS[pixels_group['ByteOrder']]
        pixel_type   = self.PIXEL_TYPES[pixels_group['Type']]
        specials     = self.SPECIAL_PIXELS[pixels_group['Type']]
        dtype        = pixel_type.newbyteorder(byte_order)

        return dtype, specials, pixels_group['Base'], pixels_group['Multiplier']

    def _get_data_start(self):
        return self.label['IsisCube']['Core']['StartByte'] - 1

    def _read_bs_data(self, stream):
        size = self.bands * self.lines * self.samples
        data = np.fromfile(stream, self.dtype, size)
        return data.reshape((self.bands, self.lines, self.samples))

    def _read_tile_data(self, stream):
        tile_lines   = self.label['IsisCube']['Core']['TileLines']
        tile_samples = self.label['IsisCube']['Core']['TileSamples']
        tile_size    = tile_samples * tile_lines

        samples = xrange(0, self.samples, tile_samples)
        lines   = xrange(0, self.lines, tile_lines)

        data = np.empty((self.bands, self.lines, self.samples),
                        dtype=self.dtype)

        for band in data:
            for line in lines:
                for sample in samples:
                    sample_end = sample + tile_samples
                    line_end   = line   + tile_lines
                    chunk      = band[line:line_end, sample:sample_end]

                    tile = np.fromfile(stream, self.dtype, tile_size)
                    tile = tile.reshape((tile_samples, tile_lines))

                    chunk_lines, chunk_samples = chunk.shape
                    chunk[:] = tile[:chunk_lines, :chunk_samples]

        return data
