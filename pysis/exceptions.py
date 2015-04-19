# -*- coding: utf-8 -*-

"""
This module contains the set of Pysis exceptions.
"""


class IsisException(Exception):
    """Base exception for isis errors."""


class VersionError(IsisException):
    """The wrong version of isis is being used."""


class ProcessError(IsisException):
    """This exception is raised when an isis process returns a non-zero exit
    status.
    """
    def __init__(self, returncode, cmd, stdout, stderr):
        self.returncode = returncode
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr

        msg = "Command '%s' returned non-zero exit status %d"
        super(ProcessError, self).__init__(msg % (self.cmd[0], self.returncode))

    def __reduce__(self):
        return (self.__class__, (
            self.returncode,
            self.cmd,
            self.stdout,
            self.stderr,
        ))
