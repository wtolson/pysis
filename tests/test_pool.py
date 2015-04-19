# -*- coding: utf-8 -*-
import pytest

from pysis import IsisPool
from pysis.exceptions import ProcessError


def test_pool():
    with IsisPool() as isis_pool:
        echo_result = isis_pool.isis_echo(hello='world')
        true_result = isis_pool.isis_true()
        false_result = isis_pool.isis_false()

    assert echo_result.get() == b'hello=world\n'
    assert true_result.get() == b''

    with pytest.raises(ProcessError):
        false_result.get()


def test_strict():
    with IsisPool(strict=True) as isis_pool:
        echo_result = isis_pool.isis_echo(hello='world')
        true_result = isis_pool.isis_true()
        false_result = isis_pool.isis_false()

    assert echo_result.get() == b'hello=world\n'
    assert true_result.get() == b''

    with pytest.raises(ProcessError):
        false_result.get()
