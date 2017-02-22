#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mmshop
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

Mickey Mouse shop
----------------
The package provides web API for a simple shop application
'''

from mmshop.settings import *

from mmshop.api import *
from mmshop.cli import *

VERSION = (0, 2, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
