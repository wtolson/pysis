# -*- coding: utf-8 -*-

"""
A pythonic syntax for calling Isis commands.
"""

import os
from os import path
from subprocess import call, check_output
from .setup import ISIS_ROOT

__all__ = [
    'Isis',
    'IsisCommand'
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
    def __init__(self, strict=False, root=ISIS_ROOT):
        self._strict = strict
        self._root = root
        self.__all__ = []

        if strict:
            self._setup_commands()

    def _setup_commands(self):
        for name, cmd in self._get_commands():
            cmd = IsisCommand(cmd)
            setattr(self, name, cmd)
            self.__all__.append(name)

    def _get_commands(self):
        # Look for commands in $ISISROOT/bin
        bin_dir = path.join(self._root, 'bin')
        for name in os.listdir(bin_dir):
            cmd = path.join(bin_dir, name)

            # Check that each file is executable and not a directory
            if path.isfile(cmd) and os.access(cmd, os.X_OK):
                yield name, cmd

    def __getattr__(self, name):
        if self._strict:
            raise AttributeError("No isis command for '%s'" % name)

        return IsisCommand(name)
