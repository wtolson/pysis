# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
A pythonic syntax for calling Isis commands.
"""

import os
import six
import subprocess

from .env import ISIS_PATH
from .exceptions import ProcessError


__all__ = [
    'Isis',
    'IsisCommand'
]


class IsisCommand(object):
    def __init__(self, name):
        self.name = name

    def cmd(self, **kwargs):
        args = [self.name]
        for (key, value) in six.iteritems(kwargs):
            args.append('%s=%s' % (key.rstrip('_'), value))
        return args

    def call(self, **kwargs):
        cmd = self.cmd(**kwargs)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            output, err = process.communicate()
        except:
            process.kill()
            process.wait()
            raise

        retcode = process.poll()
        if retcode:
            raise ProcessError(retcode, cmd, stdout=output, stderr=err)

        return output

    def to_string(self, **kwargs):
        return ' '.join(self.get_cmd(**kwargs))

    def __call__(self, **kwargs):
        return self.call(**kwargs)


class Isis(object):
    def __init__(self, strict=False, path=ISIS_PATH):
        self._strict = strict
        self._path = path

        if self._strict:
            self._setup_commands()

    def _setup_commands(self):
        for name, cmd in self._get_commands():
            self._add_command(name, cmd)

    def _get_commands(self):
        if not self._path:
            return

        for name in os.listdir(self._path):
            cmd = os.path.join(self._path, name)
            # Check that each file is executable and not a directory
            if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
                yield name, cmd

    def _add_command(self, name, cmd):
        setattr(self, name, IsisCommand(cmd))

    def __getattr__(self, name):
        if self._strict:
            return super(Isis, self).__getattr__(name)
        return IsisCommand(name)
