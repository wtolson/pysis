# -*- coding: utf-8 -*-
#
#   labels.py
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
Various Python Utilities for working with Isis labels.
"""

import re

__all__ = [
    'ParseError',
    'LabelParser',
    'get_label',
    'parse_label',
    'parse_file_label'
]

class EndFound(Exception):
    pass


class ParseError(Exception):
    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg

        super(ParseError, self).__init__()

    def __str__(self):
        return 'Line %s: %s' % (self.lineno, self.msg)


class LabelParser(object):
    unitparse = re.compile(r'^(.+)\<(.+?)\>$')
    continuation = re.compile(r'-\n')
    valid_int = re.compile(r'^[-+]?[0-9]+$')
    valid_float = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')

    def __init__(self, split_units=True, DEBUG=False):
        self.split_units = split_units
        self.DEBUG = DEBUG

        self.current_key = None

    def debug(self, msg):
        if self.DEBUG:
            print msg

    def parse(self, label):
        self.cwd = output = {}

        # Add an implecit end to the label.
        label = label + '\nEnd'

        try:
            for lineno, line in enumerate(label.splitlines(), 1):
                self.lineno = lineno
                self.debug('%s: %s' % (lineno, line))
                self.parse_line(line)

        except EndFound:
            end_found = True
            pass

        else:
            raise ParseError(lineno, 'Unexpected end of label')

        return self.format_output(output)


    def parse_line(self, line):
        line = line.strip()
        if not line or line[0] == '#':
            return

        parts = line.split('=')
        if len(parts) == 1:
            self.parse_end_group(line)

        else:
            self.parse_parts(*parts)


    def parse_end_group(self, line):
        if line == 'End_Group' or line == 'End_Object':
            if self.cwd.get('__parent__') is None:
                raise ParseError(self.lineno, 'Unexpected %s' % line)

            if line != 'End_' + self.cwd.get('__type__', ''):
                raise ParseError(self.lineno, 'Unexpected %s' % line)

            parent = self.cwd['__parent__']
            del self.cwd['__parent__']
            self.cwd = parent
            self.current_key = None

        elif line == 'End':
            if self.cwd.get('__parent__') is not None:
                raise ParseError(self.lineno, 'Unexpected End')

            self.debug('End Found')
            raise EndFound

        else:
            if self.current_key is None:
                raise ParseError(self.lineno, 'Unexpected %s' % line)

            current_value = self.cwd[self.current_key]
            if isinstance(current_value, list):
                current_value[-1] += '\n' + line

            else:
                self.cwd[self.current_key] += '\n' + line


    def parse_parts(self, key, *value):
        key = key.strip()
        value = '='.join(value).strip()

        if key == 'Object' or key == 'Group':
            obj = {'__type__': key, '__parent__': self.cwd}

            if value in self.cwd:
                if not isinstance(self.cwd[value], list):
                    self.cwd[value] = [self.cwd[value]]

                self.cwd[value].append(obj)

            else:
                self.cwd[value] = obj

            self.cwd = obj
            self.current_key = None

        else:
            units = None
            if self.split_units:
                units = self.unitparse.search(value)

            if units:
                v, u = units.groups()
                value = {'value': v, 'units': u, '__type__': 'Units'}

            if key in self.cwd:
                if not isinstance(self.cwd[key], list):
                    self.cwd[key] = [self.cwd[key]]

                self.cwd[key].append(value)

            else:
                self.cwd[key] = value

            self.current_key = key


    def format_output(self, cwd):
        for key, value in cwd.iteritems():
            cwd[key] = self.format_value(value)

        return cwd


    def format_value(self, value):
        if isinstance(value, dict):
            return self.format_output(value)

        elif isinstance(value, list):
            return [self.format_value(item) for item in value]

        else:
            return self.cast_value(value)


    def cast_value(self, value):
        value = self.continuation.sub('', value)
        value = value.strip()

        if not value or value.lower() == 'null':
            return None

        elif value[0] == '(' and value[-1] == ')':
            return [self.cast_value(item) for item in value[1:-1].split(',')]

        elif self.valid_int.match(value):
            return int(value)

        elif self.valid_float.match(value):
            return float(value)

        else:
            return value


def get_label(stream, BUF_SIZE=65537):
    """Extract the label string from an isis file.

    Arguments:
        stream: If stream is a string it will be treated as a filename other
            wise it will be treated as if it were a file object.
        BUF_SIZE: The chunksize to read the label in by.

    Returns:
        The label of the isis file as a string.
    """
    if isinstance(stream, basestring):
        with open(stream) as f:
            return get_label(f)

    label = []
    buff = stream.read(BUF_SIZE)

    while len(buff):
        label_end = buff.find('\0')

        if label_end == -1:
            label.append(buff)
        else:
            label.append(buff[:label_end])
            break

        buff = stream.read(BUF_SIZE)

    return ''.join(label)


def parse_label(label, split_units=True):
    """ Parse an isis label.

    Arguments:
        label: An isis label as a string.
        split_units: A boolean specifying whether to parse units from values.

    Returns:
        A dictionary representation of the given isis label.
    """
    return LabelParser(split_units=split_units).parse(label)


def parse_file_label(stream, split_units=True):
    """ Parse an isis label.

    Arguments:
        stream: If stream is a string it will be treated as a filename other
            wise it will be treated as if it were a file object.
        split_units: A boolean specifying whether to parse units from values.

    Returns:
        A dictionary representation of the given isis label.
    """
    return parse_label(get_label(stream), split_units=split_units)
