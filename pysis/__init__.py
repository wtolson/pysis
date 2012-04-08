# -*- coding: utf-8 -*-
import os

ISIS_ROOT = os.environ.get('ISISROOT')
if ISIS_ROOT is None:
    print 'Warning! ISISROOT is not defined. Bitch.'

    (ISIS_VERSION, ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD) = 5 * (None,)

else:
    with open(filename) as _f:
        ISIS_VERSION = _f.readline().strip()

    (ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD) = map(int, version.split('.'))


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

