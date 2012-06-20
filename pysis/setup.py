# -*- coding: utf-8 -*-
#
#   setup.py
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

import os, sys
from os import path

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

    (ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD) = map(int, ISIS_VERSION.split('.'))

except:
    sys.stderr.write('Warning! Could not find isis. Is `ISISROOT` set?\n')

    (ISIS_VERSION, ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD) = 5 * (None,)

if ISIS_VERSION_MAJOR == 3:
    #Check for the ISIS3DATA directory. If it does not exist use a default
    ISIS_DATA = path.normpath(path.join(ISIS_ROOT, '../data'))
    if not path.exists(ISIS_DATA):
        ISIS_DATA = '/usgs/cpkgs/isis3/data'
    os.environ['ISIS3DATA'] = ISIS_DATA

    #Check for the ISIS3TESTDATA directory. If it does not exist use a default
    ISIS_TEST_DATA = path.normpath(path.join(ISIS_ROOT, '../testData'))
    if not path.exists(ISIS_TEST_DATA):
        ISIS_TEST_DATA = '/usgs/cpkgs/isis3/testData'
    os.environ['ISIS3TESTDATA'] = ISIS_TEST_DATA

    #If PATH is not set, just set it to a default location. Else preappend
    #the isis path to the end of the current path
    ISIS_PATH = path.join(ISIS_ROOT, 'bin')
    if os.environ.get('PATH'):
        os.environ['PATH'] = '%s:%s' % (ISIS_ROOT, os.environ['PATH'])
    else:
        os.environ['PATH'] = ISIS_PATH

    QT_PLUGIN_PATH = path.join(ISIS_ROOT, '3rdParty/plugins')
    os.environ['QT_PLUGIN_PATH'] = QT_PLUGIN_PATH


def require_isis_version(major, minor=None, patch=None, build=None):
    err_msg = 'Version %s.%s.%s.%s of isis required (%s found).'
    err = Exception(err_msg % (major, minor, patch, build, ISIS_VERSION))

    if major != ISIS_VERSION_MAJOR:
        raise err

    if minor is not None and minor != ISIS_VERSION_MINOR:
        raise err

    if patch is not None and patch != ISIS_VERSION_PATCH:
        raise err

    if build is not None and build != ISIS_VERSION_BUILD:
        raise err

