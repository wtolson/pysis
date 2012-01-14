#!/usr/bin/env python
from multiprocessing import Pool
from subprocess import call, check_output

class IsisCommand(object):
    def __init__(self, name):
        self.name = name

    def get_cmd(self, **kwargs):
        args = [self.name]

        for (key, value) in kwargs.iteritems():
            if key[-1] == '_':
                key = key[:-1]

            args.append('%s=%s' % (key, value))

        return args

    def call(self, **kwargs):
        cmd = self.get_cmd(**kwargs)
        return call(cmd)

    def check_output(self, **kwargs):
        cmd = self.get_cmd(**kwargs)
        return check_output(cmd)


    def print_cmd(self, **kwargs):
        print ' '.join(self.get_cmd(**kwargs))

    def __call__(self, **kwargs):
        return self.call(**kwargs)



class Isis(object):
    def __getattr__(self, name):
        return IsisCommand(name)



class QueuedIsisCommand(IsisCommand):
    def __init__(self, name, queue):
        self.queue = queue
        super(QueuedIsisCommand, self).__init__(name)


    def __call__(self, **kwargs):
        return self.queue.apply_async(check_output, [self.get_cmd(**kwargs)])



class IsisPool(object):
    def __init__(self, *args, **kwargs):
        self.pool = Pool(*args, **kwargs)

    def __getattr__(self, name):
        if hasattr(self.pool, name):
            return getattr(self.pool, name)

        return QueuedIsisCommand(name, self)

    def close_and_wait(self):
        self.close()
        self.join()



isis = Isis()
