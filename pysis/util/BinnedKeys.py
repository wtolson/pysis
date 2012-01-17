# -*- coding: utf-8 -*-
#
#   BinnedKeys.py
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

"""
Flexible class for creating binned data.
"""

from math import ceil
from collections import namedtuple
from itertools import izip

__all__ = [
    'BoundsError',
    'BinnedKeys'
]

class BoundsError(IndexError):
    pass


class BinnedKeys(object):
    Item = namedtuple('Item', ['key', 'value', 'data'])
    Bounds = namedtuple('Bounds', ['min', 'max'])

    def __init__(self, min_value, max_value, num_bins=None, max_bin_size=None):
        """
        Create set of bins of the range `min_value` to `max_value` given either
        the number of bins `num_bins` or a maximum bin size `max_bin_size` with
        which to split the range.
        """
        self.min_value = float(min_value)
        self.max_value = float(max_value)

        if max_bin_size:
            num_bins = ceil((self.max_value - self.min_value) / max_bin_size)

        self.num_bins = int(num_bins)

        self.bin_size = (self.max_value - self.min_value) / self.num_bins
        self.bins = [[] for _ in xrange(self.num_bins)]


    def insert(self, key, value, data={}):
        """
        Insert the `key` into a bin based on the given `value`. Optionally,
        `data` dictionary may be provided to attach arbitrary data to the key.
        """
        item = BinnedKeys.Item(key, value, data)

        if item.value == self.max_value:
            index = self.num_bins - 1

        else:
            index = int((item.value - self.min_value) / self.bin_size)

        if index < 0 or index >= self.num_bins:
            raise BoundsError('item value out of bounds')

        self.bins[index].append(item)


    def get_bounds(self, bin_num):
        """
        Get the bonds of a bin, given its index `bin_num`. A `Bounds` namedtuple
        is returned with properties min and max respectively.
        """
        min_bound = (self.bin_size * bin_num) + self.min_value
        max_bound = min_bound + self.bin_size

        return BinnedKeys.Bounds(min_bound, max_bound)
        

    def iterkeys(self):
        """
        An iterator over the keys of each bin.
        """
        def _iterkeys(bin):
            for item in bin:
                yield item.key

        for bin in self.bins:
            yield _iterkeys(bin)


    def iterbounds(self):
        """
        An iterator over each bins bounds.
        """
        for bin_num in xrange(self.num_bins):
            yield self.get_bounds(bin_num)


    def iterbins_bounds(self):
        """
        Iterate over each bin and its bounds.
        """
        return izip(self.bins, self.iterbounds())


    def iterkeys_bounds(self):
        """
        Iterate over the keys of each bin as well as its bounds.
        """
        return izip(self.iterkeys(), self.iterbounds())
