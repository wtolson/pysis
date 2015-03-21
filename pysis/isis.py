# -*- coding: utf-8 -*-

import sys
from .setup import ISIS_VERSION
from .commands import Isis

sys.modules[__name__] = Isis(strict=(ISIS_VERSION is not None))
