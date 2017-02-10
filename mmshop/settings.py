#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mmshop.settings
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

API settings
------------
The module provides basic settings for API
'''

import os
import uuid

VERSION = (0, 1, 0)

__all__ = ['API_CONFIG', 'API_NAME', 'API_VERSION', 'API_URL',
           'API_FLAG_DEBUG']
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)


API_NAME = 'mmshop'
API_SECRET_KEY = str(uuid.uuid4())
API_VERSION = '1.0'
API_URL = '/api/v%s/%s' % (API_VERSION, API_NAME)
API_FLAG_DEBUG = True
API_CONFIG = {
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 5000,
    'request.show_tracebacks': False,
    # > Set this to True to have both errors and
    #   access messages printed to stdout
    'log.screen': False,
    # > Set this to an absolute filename where you want
    #   access messages written.
    # 'log.access_file': os.path.join('<some path>', "web.access.log"),
    # > Set this to an absolute filename where you want messages written.
    # 'log.error_file': os.path.join('<some path>', "web.error.log"),
    #
    # NO CACHE START
    'tools.response_headers.on': True,
    'tools.response_headers.headers': [
        ('Expires', 'Sun, 19 Nov 1985 05:00:00 GMT'),
        ('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'),  # @IgnorePep8
        ('Pragma', 'no-cache'),
        # ('Access-Control-Allow-Origin', '*'),
    ],
    # NO CACHE END
    #
    'tools.staticdir.root': os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'www_static'),  # @IgnorePep8
    'tools.sessions.on': True,
    'tools.sessions.storage_type': "ram",
    # 'tools.sessions.storage_type': "file",
    # 'tools.sessions.storage_path': webSessionFolder,
    #
    # SECURITY
    # 'tools.sessions.timeout': 60*24,
    # 'tools.auth_basic.on': True,
    # 'tools.auth_basic.realm': 'MMSHOP',
    # > Set here the function for authentification
    # 'tools.auth_basic.checkpassword': tools.authenticate,
}
