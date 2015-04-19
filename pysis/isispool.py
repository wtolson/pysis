# -*- coding: utf-8 -*-
from multiprocessing import Pool
from .isiscommand import Isis, IsisCommand


__all__ = [
    'IsisPool',
    'QueuedIsisCommand'
]


class QueuedIsisCommand(IsisCommand):
    def __init__(self, name, pool):
        self._pool = pool
        super(QueuedIsisCommand, self).__init__(name)

    def __call__(self, **kwds):
        return self._pool.apply_async(IsisCommand(self.name), kwds=kwds)


class IsisPool(Isis):
    """Multiprocessing pool for ISIS commands.

    Example for running the following isis script in parallel for a list of
    images.

    On the command line::

        mdis2isis from=filename.IMG to=filename.cub
        spiceinit from=filename.cub
        mdiscal from=filename.cub to=filename.cal.cub

    With pysis::

        from pysis import IsisPool
        from pysis.util import ImageName

        def calibrate_mdis(images):
            images = [ImageName(filename) for filename in images]

            with IsisPool() as isis_pool:
                for filename in images:
                    isis_pool.mdis2isis(from_=filename.IMG, to=filename.cub)

            with IsisPool() as isis_pool:
                for filename in images:
                    isis_pool.spiceinit(from_=filename.cub)

            with IsisPool() as isis_pool:
                for filename in images:
                    isis_pool.mdiscal(from_=filename.cub, to=filename.cal.cub)

    :param strict: when in strict mode, the isis pool will initialize its
        attributes with commands from the isis environment. Otherwise attributes
        are dynamically added as use

    :param **kwargs: additional parameters used to initialize the
        multiprocessing pool
    """

    def __init__(self, strict=False, *args, **kwargs):
        self._pool = Pool(*args, **kwargs)
        super(IsisPool, self).__init__(strict=strict)

    def _add_command(self, name, cmd):
        setattr(self, name, QueuedIsisCommand(cmd, self._pool))

    def __getattr__(self, name):
        return QueuedIsisCommand(name, self._pool)

    def close_and_wait(self):
        """Close the pool and wait for all commands to complete.

        This will be automatically called if used as a context manager.
        """
        self.close()
        self.join()

    def close(self, *args, **kwarg):
        self._pool.close(*args, **kwarg)

    def join(self, *args, **kwarg):
        self._pool.join(*args, **kwarg)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_and_wait()
