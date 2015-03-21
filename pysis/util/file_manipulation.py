# -*- coding: utf-8 -*-

"""
Utilities to help with file manipulation.
"""

from glob import iglob
from os.path import splitext


def write_file_list(filename, file_list=[], glob=None):
    """ Write a list of files to a file.

    Arguments:
        filename: The name of the file to write the list to.
        file_list: A list of filenames to write to a file.
        glob: If glob is specified, it will ignore file_list and instead create
            a list of files based on the pattern provide by glob (ex. *.cub).
    """
    if glob:
        file_list = iglob(glob)

    with open(filename, 'w') as f:
        for line in file_list:
            f.write(line + '\n')


def file_variations(filename, extensions):
    """ Create a variation of file names.

    Generate a list of variations on a filename by replacing the extension with
    a the provided list.

    Arguments:
        filename: The original file name to use as a base.
        extensions: A list of file extensions to generate new filenames.
    """
    (label, ext) = splitext(filename)
    return [label + extention for extention in extensions]


class ImageName(object):
    def __init__(self, base):
        self._base = base

    def __getattr__(self, name):
        return ImageName(self._base + '.' + name)

    def __str__(self):
        return str(self._base)

    def __unicode__(self):
        return unicode(self._base)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._base)
