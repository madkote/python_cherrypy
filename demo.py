#!/usr/bin/env python
# -*- coding: utf-8 -*-
# demo
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

Request demo
-----------
The module provides the functionality to make demo requests to a running API.
Demo contains following functionality:
- get all items
- get a specific item
- add new item
- update an item
- get statistics
'''

import json
import logging
import sys
import urllib.request

import mmshop

VERSION = (0, 1, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)


# =============================================================================
# UTILITIES
# =============================================================================
class RequestError(Exception):
    '''
    simple request error
    '''


def rstatus(r, data=None, method=None):
    '''
    Check the status of the HTTP response
    :param r: response
    :param data: data sent
    :param method: HTTP method the request was made
    :raise RequestError: if the response status is not positive
    '''
    s = 200
    if data:
        s = 201
    if method:
        if str(method).upper() == 'PUT':
            s = 200
    if r.status != s:
        raise RequestError('bad status: %s' % r.status)


def get_response(url, data=None, header=None, method=None):
    '''
    make HTTP request to the URL
    :param url: the URL to be requested
    :param data: data to be sent
    :param header: headers to be sent
    :param method: HTTP method to be called
    :return: the HTTP response
    :raise RequestError: if the response status is not as expected
    '''
    logging.info(' > api: %s' % url)
    req = urllib.request.Request(url)
    req_data = None
    if data is not None:
        if isinstance(data, dict):
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req_data = json.dumps(data)
        else:
            req.add_header('Content-Type', 'application/text; charset=utf-8')
            req_data = str(data)
        req_data = req_data.encode('utf-8')
        req.add_header('Content-Length', len(req_data))
        # req.method = 'POST'
    if method:
        req.method = method.upper()
    # logging.warn("*** use %s" % req.get_method())
    # logging.warn("*** use %s" % req.header_items())
    if header:
        for k, v in header:
            req.add_header(k, v)
    try:
        response = urllib.request.urlopen(req, data=req_data)
    except Exception as e:
        logging.error('*** %s %s' % (type(e), e))
        logging.error(str(e.code))
        logging.error(str(e.msg))
        logging.error(str(e.hdrs))
        logging.error(str(e.fp))
        logging.error(str(e.filename))
        raise e
    logging.info('  |_ status:  %s' % response.status)
    logging.debug('    |> url:     %s' % response.url)
    logging.debug('    |> version: %s' % response.version)
    logging.debug('    |> info:    %s' % response.info())
    rstatus(response, data=data, method=method)
    return response


# =============================================================================
# DEMO
# =============================================================================
def demo():
    '''
    Simple demo:
    - get all items
    - get a specific item
    - add new item
    - update an item
    - get statistics
    '''
    #
    #
    url = 'http://%s:%s%s' % (mmshop.API_CONFIG['server.socket_host'],
                              mmshop.API_CONFIG['server.socket_port'],
                              mmshop.API_URL)
    logging.info('')
    logging.info('=== item ===')
    logging.info(' > url: %s' % url)
    #
    # get items
    logging.info('')
    path_api = '/item'
    data = None
    header = None
    response = get_response(url + path_api, data=data, header=header)
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)
    #
    # get item by id
    logging.info('')
    path_api = '/item/1'
    data = None
    header = None
    response = get_response(url + path_api, data=data, header=header)
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)
    #
    # new item
    logging.info('')
    path_api = '/item'
    data = {'name': 'banana', 'price': 0.29}
    header = None
    response = get_response(url + path_api, data=data, header=header)
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)
    #
    # get items
    logging.info('')
    path_api = '/item'
    data = None
    header = None
    response = get_response(url + path_api, data=data, header=header)
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)
    #
    # update item
    logging.info('')
    path_api = '/item/3'
    data = {'name': 'mouse', 'price': 10.99}
    header = None
    response = get_response(url + path_api,
                            data=data,
                            header=header,
                            method='PUT')
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)
    #
    # get items
    logging.info('')
    path_api = '/item'
    data = None
    header = None
    response = get_response(url + path_api, data=data, header=header)
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)
    #
    # statistics (dummy)
    logging.info('')
    path_api = '/stats'
    data = None
    header = None
    response = get_response(url + path_api, data=data, header=header)
    data = json.loads(response.read().decode())
    logging.info(' > res: %s' % type(data))
    logging.info(' > res: %s' % data)


if __name__ == '__main__':
    if 'debug' in sys.argv:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)
    try:
        demo()
    finally:
        logging.shutdown()
