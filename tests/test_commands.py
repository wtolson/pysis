# -*- coding: utf-8 -*-
import pytest

from pysis import Isis
from pysis.exceptions import ProcessError


def test_true():
    isis = Isis(strict=True)
    assert isis.isis_true() == b''


def test_false():
    isis = Isis(strict=True)
    with pytest.raises(ProcessError):
        isis.isis_false()


def test_echo():
    isis = Isis(strict=True)
    assert isis.isis_echo() == b'\n'
    assert isis.isis_echo(from_='to') == b'from=to\n'

    output = isis.isis_echo(foo='bar', baz='bang').split()
    assert len(output) == 2
    assert b'foo=bar' in output
    assert b'baz=bang' in output


def test_strict():
    isis = Isis(strict=True)
    with pytest.raises(AttributeError):
        isis.ls()


def test_lazy():
    isis = Isis(strict=False)
    assert isis.isis_true() == b''
    with pytest.raises(ProcessError):
        isis.isis_false()


def test_isis_module():
    from pysis import isis
    assert isis.isis_true() == b''

    from pysis.isis import isis_true
    assert isis_true() == b''
