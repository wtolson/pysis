# -*- coding: utf-8 -*-
#
#   GeometricBinnedKeys.py
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


from math import log, ceil
from AbstractBinnedKeys import AbstractBinnedKeys


class GeometricBinnedKeys(AbstractBinnedKeys):
    """
    A Binned Keys construct for creating geometrically binned data.
    """

    C = 2.0 / log(2.0)

    def __init__(self, min_value, max_value):
        """
        Create set of bins including the values `min_value` and `max_value` such
        that the bin boundaries for bin[i + 1] and bin[i] have the ratio of
        sqrt(2).
        """

        self.min_value = float(min_value)

        self.num_bins = ceil(GeometricBinnedKeys.C * log(max_value / self.min_value))
        self.max_value = pow(2.0, self.num_bins / 2.0) * self.min_value
        self.num_bins = int(self.num_bins)

        self.bins = [[] for _ in xrange(self.num_bins)]


    def get_bin_index(self, value):
        """
        Used to get the index of the bin to place a particular value.
        """
        if value == self.max_value:
            return self.num_bins - 1
        
        return int(GeometricBinnedKeys.C * log(value / self.min_value))


    def get_bounds(self, bin_num):
        """
        Get the bonds of a bin, given its index `bin_num`. A `Bounds` namedtuple
        is returned with properties min and max respectively.
        """
        min_value = pow(2.0, float(bin_num) / 2.0) * self.min_value
        max_value = pow(2.0, float(bin_num + 1.0) / 2.0) * self.min_value

        return GeometricBinnedKeys.Bounds(min_value, max_value)
