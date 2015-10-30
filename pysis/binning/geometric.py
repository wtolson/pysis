# -*- coding: utf-8 -*-

from math import log, ceil
from six.moves import range
from .abstract import AbstractBinnedKeys


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

        self.num_bins = ceil(self.C * log(max_value / self.min_value))
        self.max_value = pow(2.0, self.num_bins / 2.0) * self.min_value
        self.num_bins = int(self.num_bins)

        self.bins = [[] for _ in range(self.num_bins)]

    def get_bin_index(self, value):
        """Used to get the index of the bin to place a particular value."""
        if value == self.max_value:
            return self.num_bins - 1

        return int(self.C * log(value / self.min_value))

    def get_bounds(self, bin_num):
        """Get the bonds of a bin, given its index `bin_num`.

        :returns: a `Bounds` namedtuple with properties min and max
            respectively.
        """
        min_value = pow(2.0, float(bin_num) / 2.0) * self.min_value
        max_value = pow(2.0, float(bin_num + 1.0) / 2.0) * self.min_value
        return self.Bounds(min_value, max_value)
