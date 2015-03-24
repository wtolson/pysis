# -*- coding: utf-8 -*-
import pytest
import subprocess
from pysis.commands import Isis


def test_true():
    isis = Isis(strict=True)
    assert isis.isis_true() == 0
    assert isis.isis_true.check_output() == ''


def test_false():
    isis = Isis(strict=True)
    assert isis.isis_false() == 1

    with pytest.raises(subprocess.CalledProcessError):
        isis.isis_false.check_output()


def test_echo():
    isis = Isis(strict=True)
    assert isis.isis_echo(foo='bar') == 0
    assert isis.isis_echo.check_output() == '\n'
    assert isis.isis_echo.check_output(from_='to') == 'from=to\n'

    output = isis.isis_echo.check_output(foo='bar', baz='bang').split()
    assert len(output) == 2
    assert 'foo=bar' in output
    assert 'baz=bang' in output


def test_strict():
    isis = Isis(strict=True)
    with pytest.raises(AttributeError):
        isis.ls()


def test_lazy():
    isis = Isis(strict=False)
    assert isis.isis_true() == 0
    assert isis.isis_false() == 1
