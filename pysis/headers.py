#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   isis_utils.py
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
#

"""
Various Python Utilities for working with Isis headers.
"""

import re

class EndFound(Exception):
    pass


class HeaderParser(object):
    unitparse = re.compile(r'^(.+)\<(.+?)\>$')
    continuation = re.compile(r'-\n')
    valid_int = re.compile(r'^[-+]?[0-9]+$')
    valid_float = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')

    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG

    def debug(self, msg):
        if self.DEBUG:
            print msg

    def parse(self, header):
        self.output = {}
        self.cwd = self.output
        end_found = False

        lines = header.splitlines()
        try:
            for line_no, line in enumerate(lines, 1):
                self.line_no = line_no
                self.debug('%s: %s' % (line_no, line))
                self.parse_line(line)

        except EndFound:
            end_found = True
            pass

        if not end_found:
            raise Exception('Unexpected end of header')

        self.format_output(self.output)
        return self.output


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
                raise Exception('%s: Unexpected %s' % (self.line_no, line))

            parent = self.cwd['__parent__']
            del self.cwd['__parent__']
            self.cwd = parent
            self.current_key = None

        elif line == 'End':
            if self.cwd.get('__parent__') is not None:
                raise Exception('%s: Unexpected End' % self.line_no)

            self.debug('End Found')
            raise EndFound

        else:
            if self.current_key is None:
                raise Exception('%s: Unexpected %s' % (self.line_no, line))

            current_value = self.cwd[self.current_key]
            if isinstance(current_value, list):
                current_value[-1] += '\n' + line

            else:
                self.cwd[self.current_key] += '\n' + line



    def parse_parts(self, key, *value):
        key = key.strip()
        value = '='.join(value).strip()

        if key == 'Object' or key == 'Group':
            if value in self.cwd:
                if not isinstance(self.cwd[value], list):
                    self.cwd[value] = [self.cwd[value]]

                self.cwd[value].append({'__parent__': self.cwd})
                self.cwd = self.cwd[value][-1]

            else:
                self.cwd[value] = {'__parent__': self.cwd}
                self.cwd = self.cwd[value]
            
            self.current_key = None

        else:
            units = self.unitparse.search(value)
            if units:
                v, u = units.groups()
                value = {'value': v, 'units': u}

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



def get_header(filename):
    """Gets the header of the specified isis file."""

    BUF_SIZE = 65537
    unitparse = re.compile(r'^(.+)\<(.+?)\>$')

    header = []
    with open(filename) as f:
        buff = f.read(BUF_SIZE)
        while len(buff):
            if '\0' in buff:
                header.append(buff.split('\0')[0])
                break
            else:
                header.append(buff)

            buff = f.read(BUF_SIZE)

    return ''.join(header)



_parser = HeaderParser()
def parse_header(header):
    return _parser.parse(header)


def parse_file_header(filename):
    """Returns a dictionary representation of the givin isis file's header."""
    return parse_header(get_header(filename))
