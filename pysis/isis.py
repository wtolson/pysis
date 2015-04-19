# -*- coding: utf-8 -*-
import sys
import types

from .env import ISIS_VERSION
from .isiscommand import Isis


class ModuleWrapper(Isis, types.ModuleType):
    def __init__(self, self_module, **kwargs):
        # this is super ugly to have to copy attributes like this,
        # but it seems to be the only way to make reload() behave
        # nicely.  if i make these attributes dynamic lookups in
        # __getattr__, reload sometimes chokes in weird ways...
        for attr in ['__builtins__', '__doc__', '__name__', '__package__']:
            setattr(self, attr, getattr(self_module, attr, None))

        # python 3.2 (2.7 and 3.3 work fine) breaks on osx (not ubuntu)
        # if we set this to None.  and 3.3 needs a value for __path__
        self.__path__ = []
        self.__all__ = []
        self.__self_module = self_module

        super(ModuleWrapper, self).__init__(**kwargs)

    def __getattr__(self, name):
        try:
            return getattr(self.__self_module, name)
        except AttributeError:
            return super(Isis, self).__getattr__(name)

    def _add_command(self, name, cmd):
        super(ModuleWrapper, self)._add_command(name, cmd)
        self.__all__.append(name)


sys.modules[__name__] = ModuleWrapper(
    self_module=sys.modules[__name__],
    strict=(ISIS_VERSION is not None),
)
