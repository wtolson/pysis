# -*- coding: utf-8 -*-

import os
from os import path
from functools import wraps

from .exceptions import VersionError

__all__ = [
    'ISIS_ROOT',
    'ISIS_VERSION',
    'ISIS_VERSION_MAJOR',
    'ISIS_VERSION_MINOR',
    'ISIS_VERSION_PATCH',
    'ISIS_VERSION_BUILD',
    'require_isis_version'
]

ISIS_ROOT = os.environ.setdefault('ISISROOT', '/usgs/pkgs/isis3/isis')
try:
    with open(path.join(ISIS_ROOT, 'version')) as _f:
        ISIS_VERSION = _f.readline().strip()

    ISIS_VERISON_TUPLE = tuple(map(int, ISIS_VERSION.split('.')))

    (
        ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD
    ) = ISIS_VERISON_TUPLE

except:
    import warnings
    warnings.warn('Could not find isis. Is `ISISROOT` set?', RuntimeWarning)

    (ISIS_VERSION, ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD) = 5 * (None,)

if ISIS_VERSION_MAJOR == 3:
    # Check for the ISIS3DATA directory. If it does not exist use a default
    ISIS_DATA = path.normpath(path.join(ISIS_ROOT, '../data'))
    if not path.exists(ISIS_DATA):
        ISIS_DATA = '/usgs/cpkgs/isis3/data'
    os.environ['ISIS3DATA'] = ISIS_DATA

    # Check for the ISIS3TESTDATA directory. If it does not exist use a default
    ISIS_TEST_DATA = path.normpath(path.join(ISIS_ROOT, '../testData'))
    if not path.exists(ISIS_TEST_DATA):
        ISIS_TEST_DATA = '/usgs/cpkgs/isis3/testData'
    os.environ['ISIS3TESTDATA'] = ISIS_TEST_DATA

    # If PATH is not set, just set it to a default location. Else preappend
    # the isis path to the end of the current path
    ISIS_PATH = path.join(ISIS_ROOT, 'bin')
    if os.environ.get('PATH'):
        os.environ['PATH'] = '%s:%s' % (ISIS_PATH, os.environ['PATH'])
    else:
        os.environ['PATH'] = ISIS_PATH

    QT_PLUGIN_PATH = path.join(ISIS_ROOT, '3rdParty/plugins')
    os.environ['QT_PLUGIN_PATH'] = QT_PLUGIN_PATH

else:
    ISIS_DATA = None
    ISIS_TEST_DATA = None
    ISIS_PATH = None
    QT_PLUGIN_PATH = None


def check_isis_version(major, minor=0, patch=0, build=0):
    """Checks that the current isis version is equal to or above the suplied
    version."""
    if ISIS_VERSION and (major, minor, patch, build) <= ISIS_VERISON_TUPLE:
        return

    msg = 'Version %s.%s.%s.%s of isis required (%s found).'
    raise VersionError(msg % (major, minor, patch, build, ISIS_VERSION))


def require_isis_version(major, minor=0, patch=0, build=0):
    """Decorator that ensures a function is called with a minimum isis version.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            check_isis_version(major, minor, patch, build)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
