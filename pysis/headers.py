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

import yaml, re

class EndFound(Exception):
    pass


class HeaderParser(object):
    unitparse = re.compile(r'^(.+)\<(.+?)\>$')

    def __init__(self, indent=' ', DEBUG=False):
        self.indent = indent
        self.DEBUG = DEBUG

    def debug(self, msg):
        if self.DEBUG:
            print msg

    def parse(self, header):
        self.level = 0

        lines = header.splitlines()
        output = []
        end_found = False

        try:
            for line_no, line in enumerate(lines, 1):
                self.line_no = line_no
                self.debug('%s: %s' % (line_no, line))
                output.append(self.parse_line(line))

        except EndFound:
            end_found = True
            pass

        if not end_found:
            raise Exception('Unexpected end of header')

        return '\n'.join(output)


    def parse_line(self, line):
        line = line.strip()
        if not line or line[0] == '#':
            return line

        parts = line.split('=')
        if len(parts) == 1:
            return self.parse_end_group(line)

        else:
            return self.parse_parts(*parts)


    def parse_end_group(self, line):
        if line == 'End_Group' or line == 'End_Object':
            if self.level <= 0:
                raise Exception('%s: Unexpected %s' % (self.line_no, line))

            self.debug('End of level %s' % self.level)
            self.level -= 1

        elif line == 'End':
            if self.level != 0:
                raise Exception('%s: Unexpected End' % self.line_no)

            self.debug('End Found')
            raise EndFound

        else:
            raise Exception('%s: Unexpected %s' % (self.line_no, line))

        return ''

    def parse_parts(self, key, *value):
        key = key.strip()
        value = '='.join(value).strip()

        if key == 'Object' or key == 'Group':
            line = '%s%s:' % (self.level * self.indent, value)
            self.level += 1
            self.debug('Start of level %s' % self.level)

        else:
            self.debug('Got key/vaue: %s/%s' % (key, value))
            units = self.unitparse.search(value)
            if units:
                value, units = units.groups()
                line = '\n'.join([
                    '%s%s:' % (self.level * self.indent, key),
                    '%svalue: %s' % ((self.level + 1) * self.indent, value),
                    '%sunit: %s' % ((self.level + 1) * self.indent, units)
                ])

            else:
                line = '%s%s: %s' % (self.level * self.indent, key, value)

        return line


def get_header(filename):
    """Gets the header of the specified isis file."""

    BUF_SIZE = 65537
    unitparse = re.compile(r'^(.+)\<(.+?)\>$')

    header = []
    with open(filename) as f:
        buff = f.read(BUF_SIZE)
        while len(buff):
            if "\0" in buff:
                header.append(buff.split("\0")[0])
                break
            else:
                header.append(buff)

            buff = f.read(BUF_SIZE)

    return "".join(header)



_parser = HeaderParser()
def header2yaml(header):
    return _parser.parse(header)


def parse_header(header):
    return yaml.load(header2yaml(header))


def parse_file_header(filename):
    """Returns a dictionary representation of the givin isis file's header."""
    return parse_header(get_header(filename))
