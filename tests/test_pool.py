# -*- coding: utf-8 -*-
from pysis import IsisPool


def test_pool():
    with IsisPool() as isis_pool:
        res1 = isis_pool.isis_echo(count=1)
        res2 = isis_pool.isis_echo(count=2)
        res3 = isis_pool.isis_echo(count=3)

    assert res1.get() == 'count=1\n'
    assert res2.get() == 'count=2\n'
    assert res3.get() == 'count=3\n'
