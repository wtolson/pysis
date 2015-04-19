# -*- coding: utf-8 -*-

import sys
from .env import ISIS_VERSION
from .command import Isis

sys.modules[__name__] = Isis(strict=(ISIS_VERSION is not None))
