# -*- coding: utf-8 -*-
#
#   BoundedBinnedKeys.py
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

from bisect import bisect
from AbstractBinnedKeys import AbstractBinnedKeys


class BoundedBinnedKeys(AbstractBinnedKeys):
    """
    A Binned Keys construct where bins are defined by a list of their bounds.
    """

    def __init__(self, bounds):
        """
        Create set of bins with the bin boundaries for bin[i] being bounds[i] to
        to bounds[i + 1]. The list `bounds` must be monotonically increasing.
        """
        self.bounds = bounds

        self.min_value = bounds[0]
        self.max_value = bounds[-1]

        self.num_bins = len(bounds) - 1
        self.bins = [[] for _ in xrange(self.num_bins)]


    def get_bin_index(self, value):
        """
        Used to get the index of the bin to place a particular value.
        """
        return bisect(self.bounds, value) - 1


    def get_bounds(self, bin_num):
        """
        Get the bonds of a bin, given its index `bin_num`. A `Bounds` namedtuple
        is returned with properties min and max respectively.
        """
        return LooseBinnedKeys.Bounds(*self.bounds[bin_num:bin_num+2])
