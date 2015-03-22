import os
import pytest

from pysis import (
    ISIS_ROOT,
    ISIS_VERSION,
    ISIS_VERSION_MAJOR,
    ISIS_VERSION_MINOR,
    ISIS_VERSION_PATCH,
    ISIS_VERSION_BUILD,
    require_isis_version,
)

from pysis.exceptions import VersionError


def test_root():
    assert ISIS_ROOT == os.environ['ISISROOT']


def test_path():
    assert os.path.join(ISIS_ROOT, 'bin') in os.environ['PATH'].split(':')


def test_version():
    assert isinstance(ISIS_VERSION_MAJOR, int)
    assert isinstance(ISIS_VERSION_MINOR, int)
    assert isinstance(ISIS_VERSION_PATCH, int)
    assert isinstance(ISIS_VERSION_BUILD, int)
    assert ISIS_VERSION == '%d.%d.%d.%d' % (
        ISIS_VERSION_MAJOR, ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH, ISIS_VERSION_BUILD
    )


def test_require_isis_version():
    with pytest.raises(VersionError):
        require_isis_version(ISIS_VERSION_MAJOR - 1)
