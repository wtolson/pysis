# -*- coding: utf-8 -*-
#
#   file_manipulation.py
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
Utilities to help with file manipulation.
"""

from glob import iglob
from os.path import splitext

__all__ = [
    'write_file_list',
    'file_variations'
]

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
        extensions: A list of file extensions to to generate new filenames.
    """
    (label, ext) = splitext(filename)
    return [label + extention for extention in extensions]
