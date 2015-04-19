# -*- coding: utf-8 -*-

import sys
from .commands import Isis
from .env import ISIS_VERSION

sys.modules[__name__] = Isis(strict=(ISIS_VERSION is not None))
