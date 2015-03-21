# -*- coding: utf-8 -*-

"""
This module contains the set of Pysis exceptions.
"""


class IsisException(Exception):
    """ Base exception for isis errors. """


class VersionError(IsisException):
    """ The wrong version of isis is being used. """
