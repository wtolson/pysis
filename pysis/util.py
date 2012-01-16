# -*- coding: utf-8 -*-
#
#   util.py
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
Utilities to help with common Isis patterns.
"""

from glob import iglob
from os.path import splitext

def write_file_list(filename, file_list=[], glob=None):
    """
    Write a list of files to a file.
    """
    if glob:
        file_list = iglob(glob)

    with open(filename, 'w') as f:
        for line in file_list:
            f.write(line + '\n')


def file_variations(filename, extentions):
    """
    Generate a list of variations on a filename by replacing the extention with
    a the provided list.
    """
    (label, ext) = splitext(filename)
    return [label + extention for extention in extentions]
