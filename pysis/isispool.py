# -*- coding: utf-8 -*-

""" Simple multiprocessing for Isis commands.

Usage:
    Example for running the following isis script in parallel for a list of
    images.

        mdis2isis from=filename.IMG to=filename.cub
        spiceinit from=filename.cub
        mdiscal from=filename.cub to=filename.cal.cub

    from pysis import IsisPool
    from pysis.util import file_variations

    def calibrate_mdis(images):
        images = [(img_name,) + file_variations(img_name, ['.cub', '.cal.cub'])
                    for img_name in images]

        with IsisPool() as isis_pool:
            for img_name, cub_name, cal_name in images:
                isis_pool.mdis2isis(from_=img_name, to=cub_name)

        with IsisPool() as isis_pool:
            for img_name, cub_name, cal_name in images:
                isis_pool.spiceinit(from_=cub_name)

        with IsisPool() as isis_pool:
            for img_name, cub_name, cal_name in images:
                isis_pool.mdiscal(from_=cub_name, to=cal_name)

"""
from multiprocessing import Pool
from subprocess import check_output

from .commands import Isis
from .commands import IsisCommand

__all__ = [
    'IsisPool',
    'QueuedIsisCommand'
]


class QueuedIsisCommand(IsisCommand):
    def __init__(self, name, queue):
        self.queue = queue
        super(QueuedIsisCommand, self).__init__(name)

    def __call__(self, **kwargs):
        return self.queue.apply_async(check_output, [self.get_cmd(**kwargs)])


class IsisPool(Isis):
    def __init__(self, strict=False, *args, **kwargs):
        self.pool = Pool(*args, **kwargs)

        self._strict = strict
        if strict:
            for name, cmd in self._get_commands():
                cmd = QueuedIsisCommand(cmd)
                setattr(self, name, cmd)

    def __getattr__(self, name):
        if hasattr(self.pool, name):
            return getattr(self.pool, name)

        if self._strict:
            raise AttributeError("No isis command for '%s'" % name)

        return QueuedIsisCommand(name, self)

    def close_and_wait(self):
        self.close()
        self.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_and_wait()
