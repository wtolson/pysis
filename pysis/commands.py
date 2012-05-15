# -*- coding: utf-8 -*-
#
#   commands.py
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
A pythonic syntax for calling Isis commands.
"""
import os
from os import path
from multiprocessing import Pool
from subprocess import call, check_output
from .setup import ISIS_ROOT

__all__ = [
    'Isis',
    'IsisCommand',
    'IsisPool',
    'QueuedIsisCommand'
]

class IsisCommand(object):
    def __init__(self, name):
        self.name = name

    def get_cmd(self, **kwargs):
        args = [self.name]

        for (key, value) in kwargs.iteritems():
            if key[-1] == '_':
                key = key[:-1]

            args.append('%s=%s' % (key, value))

        return args

    def call(self, **kwargs):
        cmd = self.get_cmd(**kwargs)
        return call(cmd)

    def check_output(self, **kwargs):
        cmd = self.get_cmd(**kwargs)
        return check_output(cmd)

    def print_cmd(self, **kwargs):
        print ' '.join(self.get_cmd(**kwargs))

    def __call__(self, **kwargs):
        return self.call(**kwargs)


class Isis(object):
    @staticmethod
    def _get_commands():
        bin_dir = path.join(ISIS_ROOT, 'bin')
        for name in os.listdir(bin_dir):
            cmd = path.join(bin_dir, name)
            if path.isfile(cmd) and os.access(cmd, os.X_OK):
                yield name, cmd

    def __init__(self, strict=False):
        self._strict = strict
        self.__all__ = []
        if strict:
            for name, cmd in self._get_commands():
                cmd = IsisCommand(cmd)
                setattr(self, name, cmd)
                self.__all__.append(name)

    def __getattr__(self, name):
        if self._strict:
            raise AttributeError("No isis command for '%s'" % name)

        return IsisCommand(name)


class QueuedIsisCommand(IsisCommand):
    def __init__(self, name, queue):
        self.queue = queue
        super(QueuedIsisCommand, self).__init__(name)

    def __call__(self, **kwargs):
        return self.queue.apply_async(check_output, [self.get_cmd(**kwargs)])


class IsisPool(Isis):
    def __init__(self, strict=False, *args, **kwargs):
        self.pool = Pool(*args, **kwargs)

        self._strict = strict
        if strict:
            for name, cmd in self._get_commands():
                cmd = QueuedIsisCommand(cmd)
                setattr(self, name, cmd)

    def __getattr__(self, name):
        if hasattr(self.pool, name):
            return getattr(self.pool, name)

        if self._strict:
            raise AttributeError("No isis command for '%s'" % name)

        return QueuedIsisCommand(name, self)

    def close_and_wait(self):
        self.close()
        self.join()

