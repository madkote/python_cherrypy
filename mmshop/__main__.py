#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mmshop.__main__
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

Main
----
The main entry point for the package
'''

import sys

import mmshop

VERSION = (0, 1, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)


if __name__ == '__main__':
    sys.exit(mmshop.main())
