import os
import pytest

from pysis import (
    ISIS_ROOT,
    ISIS_VERSION,
    ISIS_VERSION_MAJOR,
    ISIS_VERSION_MINOR,
    ISIS_VERSION_PATCH,
    ISIS_VERSION_BUILD,
    check_isis_version,
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


def test_check_isis_version():
    check_isis_version(ISIS_VERSION_MAJOR - 1)
    check_isis_version(ISIS_VERSION_MAJOR)
    check_isis_version(
        ISIS_VERSION_MAJOR,
        ISIS_VERSION_MINOR,
        ISIS_VERSION_PATCH,
        ISIS_VERSION_BUILD,
    )

    with pytest.raises(VersionError):
        check_isis_version(ISIS_VERSION_MAJOR + 1)

    with pytest.raises(VersionError):
        check_isis_version(
            ISIS_VERSION_MAJOR + 1,
            ISIS_VERSION_MINOR,
            ISIS_VERSION_PATCH,
            ISIS_VERSION_BUILD,
        )

    with pytest.raises(VersionError):
        check_isis_version(
            ISIS_VERSION_MAJOR,
            ISIS_VERSION_MINOR + 1,
            ISIS_VERSION_PATCH,
            ISIS_VERSION_BUILD,
        )

    with pytest.raises(VersionError):
        check_isis_version(
            ISIS_VERSION_MAJOR,
            ISIS_VERSION_MINOR,
            ISIS_VERSION_PATCH + 1,
            ISIS_VERSION_BUILD,
        )

    with pytest.raises(VersionError):
        check_isis_version(
            ISIS_VERSION_MAJOR,
            ISIS_VERSION_MINOR,
            ISIS_VERSION_PATCH,
            ISIS_VERSION_BUILD + 1,
        )


def test_require_isis_version():

    @require_isis_version(ISIS_VERSION_MAJOR)
    def echo(x):
        return x

    @require_isis_version(ISIS_VERSION_MAJOR + 1)
    def random_number():
        return 4  # chosen by fail dice roll, guaranteed to be random

    assert echo(42) == 42

    with pytest.raises(VersionError):
        random_number()
