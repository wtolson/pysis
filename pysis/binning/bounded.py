# -*- coding: utf-8 -*-

from bisect import bisect
from six.moves import range
from .abstract import AbstractBinnedKeys


class BoundedBinnedKeys(AbstractBinnedKeys):
    """A Binned Keys construct where bins are defined by a list of their bounds.
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
        self.bins = [[] for _ in range(self.num_bins)]

    def get_bin_index(self, value):
        """Used to get the index of the bin to place a particular value."""
        return bisect(self.bounds, value) - 1

    def get_bounds(self, bin_num):
        """Get the bonds of a bin, given its index `bin_num`.

        :returns: a `Bounds` namedtuple with properties min and max
            respectively.
        """
        return self.Bounds(*self.bounds[bin_num:bin_num + 2])
