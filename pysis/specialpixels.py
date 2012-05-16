# -*- coding: utf-8 -*-
#
#   specialpixels.py
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

""" Constants for Isis Special Pixels.

    Min:  The minimum valid value for a pixel.
    Null: Pixel has no data available.
    Lis:  Pixel was lower bound saturated on the instrument.
    His:  Pixel was higher bound saturated on the instrument.
    Lrs:  Pixel was lower bound saturated during a computation.
    Hrs:  Pixel was higher bound saturated during a computation.
    Max:  The maximum valid value for a pixel.
"""

import numpy as np

__all__ = ['SPECIAL_PIXELS']

def _make_num(num, dtype):
    return np.fromstring(num, dtype=dtype)[0]

SPECIAL_PIXELS = {

    'UnsignedByte': {
        'Min':    1,
        'Null':   0,
        'Lrs':    0,
        'Lis':    0,
        'His':  255,
        'Hrs':  255,
        'Max':  254
    },

    'UnsignedWord': {
        'Min':      3,
        'Null':     0,
        'Lrs':      1,
        'Lis':      2,
        'His':  65534,
        'Hrs':  65535,
        'Max':  65522
    },

    'SignedWord': {
        'Min':  -32752,
        'Null': -32768,
        'Lrs':  -32767,
        'Lis':  -32766,
        'His':  -32765,
        'Hrs':  -32764,
        'Max':   32767
    },

    'SignedInteger': {
        'Min':   -8388614,
        'Null':  -8388613,
        'Lrs':   -8388612,
        'Lis':   -8388611,
        'His':   -8388610,
        'Hrs':   -8388609,
        'Max': 2147483647
    },

    'Real': {
        'Min':  _make_num('\xFF\x7F\xFF\xFA', '>f4'),
        'Null': _make_num('\xFF\x7F\xFF\xFB', '>f4'),
        'Lrs':  _make_num('\xFF\x7F\xFF\xFC', '>f4'),
        'Lis':  _make_num('\xFF\x7F\xFF\xFD', '>f4'),
        'His':  _make_num('\xFF\x7F\xFF\xFE', '>f4'),
        'Hrs':  _make_num('\xFF\x7F\xFF\xFF', '>f4'),
        'Max':  np.finfo('f4').max
    },

    'Double': {
        'Min':  _make_num('\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFA', '>f8'),
        'Null': _make_num('\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFB', '>f8'),
        'Lrs':  _make_num('\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFC', '>f8'),
        'Lis':  _make_num('\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFD', '>f8'),
        'His':  _make_num('\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFE', '>f8'),
        'Hrs':  _make_num('\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFF', '>f8'),
        'Max':  np.finfo('f8').max
    }
}
