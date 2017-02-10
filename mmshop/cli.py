#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mmshop.cli
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

Application runner
------------------
The module provides basic application runner with parameters
'''

import argparse
import cherrypy
import logging
import os
import sys

import mmshop

VERSION = (0, 1, 0)

__all__ = ['main', 'quick_start']
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)

DEBUG = 0
TESTRUN = 0
PROFILE = 0

DESCRIPTION = 'Mickey Mouse shop web API'


# =============================================================================
# API SEVICE STARTER
# =============================================================================
def quick_start(host=None, port=None, level=None):
    '''
    Start server
    :param host: host name
    :param port: port to be exposed
    :param level: logging level
    '''
    #
    # logging
    if not level:
        level = logging.WARNING
    logging.basicConfig(level=level, stream=sys.stdout)
    #
    # settings
    app = mmshop.MickeyMouseShop
    script_name = mmshop.API_URL
    config = dict(mmshop.API_CONFIG)
    if host:
        config['server.socket_host'] = str(host)
    if port:
        config['server.socket_port'] = int(port)
    #
    # apply configurations
    cherrypy.log.access_log.level = logging.ERROR
    if config:
        cherrypy.config.update(config)
    #
    # the autoreloader restarts the webserver automatically as soon
    # as a source file has changed
    # deactivates the autoreloader
    # cherrypy.engine.autoreload.unsubscribe()
    #
    # run service
    cherrypy.quickstart(root=app(), script_name=script_name, config=None)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================
def main(argv=None):
    '''
    Command line interface main
    :param argv: arguments
    :return: the program exit code
    '''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    program_name = os.path.basename(sys.argv[0])
    indent = len(program_name) * ' '
    res = 0
    try:
        #
        # parser
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            action='count',
                            help='set verbosity level')
        parser.add_argument('-V', '--version',
                            action='version',
                            version=mmshop.__version__)
        parser.add_argument('--host',
                            dest='host',
                            action='store',
                            default=None,
                            help='Host name')
        parser.add_argument('--port',
                            dest='port',
                            action='store',
                            default=None,
                            help='Port')
        #
        # Process arguments
        args = parser.parse_args()
        verbose = args.verbose
        host = args.host
        port = args.port
        #
        # settings
        if verbose == 0:
            level = logging.WARNING
        elif verbose == 1:
            level = logging.INFO
        else:
            level = logging.DEBUG
        #
        # run API service
        quick_start(host, port, level)
    except KeyboardInterrupt:
        res = 1
        print(program_name + ': ')
        print(indent + '  user abort')
    except Exception as e:
        res = 2
        print(program_name + ': ')
        print(indent + '  error %s' % repr(e))
        if DEBUG or TESTRUN:
            raise(e)
    finally:
        return res


if __name__ == '__main__':
    if DEBUG:
        sys.argv.append('-h')
        sys.argv.append('-v')
        sys.argv.append('-r')
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'demo_request_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
