# -*- coding: utf-8 -*-

from collections import namedtuple
from itertools import izip
from abc import ABCMeta, abstractmethod
from six.moves import range


__all__ = [
    'BoundsError',
    'AbstractBinnedKeys'
]


class BoundsError(IndexError):
    pass


class AbstractBinnedKeys(object):
    """Flexible base class for binning data."""
    __metaclass__ = ABCMeta

    Item = namedtuple('Item', ['key', 'value', 'data'])
    Bounds = namedtuple('Bounds', ['min', 'max'])

    @abstractmethod
    def get_bin_index(self, value):
        """Get the index of the bin to place a particular value."""
        pass

    @abstractmethod
    def get_bounds(self, bin_num):
        """Get the bounds of a bin, given its index `bin_num`.

        :returns: a `Bounds` namedtuple with properties min and max
            respectively.
        """
        pass

    def insert(self, key, value, data={}):
        """Insert the `key` into a bin based on the given `value`.

        Optionally, `data` dictionary may be provided to attach arbitrary data
        to the key.
        """
        if value < self.min_value or value > self.max_value:
            raise BoundsError('item value out of bounds')

        item = self.Item(key, value, data)
        index = self.get_bin_index(value)

        self.bins[index].append(item)

    def iterkeys(self):
        """An iterator over the keys of each bin."""
        def _iterkeys(bin):
            for item in bin:
                yield item.key

        for bin in self.bins:
            yield _iterkeys(bin)

    def iterbounds(self):
        """An iterator over each bins bounds."""
        for bin_num in range(self.num_bins):
            yield self.get_bounds(bin_num)

    def iterbins_bounds(self):
        """Iterate over each bin and its bounds."""
        return izip(self.bins, self.iterbounds())

    def iterkeys_bounds(self):
        """Iterate over the keys of each bin as well as its bounds."""
        return izip(self.iterkeys(), self.iterbounds())
