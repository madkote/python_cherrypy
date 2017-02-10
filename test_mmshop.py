#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_mmshop
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

Test
----
Test module for the Mickey Mouse shop
'''

import cherrypy
import json
import unittest
import urllib.request

import mmshop

VERSION = (0, 1, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)


class _TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''
        configure and start service
        '''
        app = mmshop.MickeyMouseShop
        script_name = mmshop.API_URL
        config = dict(mmshop.API_CONFIG)
        cherrypy.config.update(config)
        cherrypy.engine.autoreload.unsubscribe()
        cherrypy.tree.mount(app(), script_name)
        cherrypy.server.unsubscribe()
        cherrypy.engine.start()
        cherrypy.server.start()

    @classmethod
    def tearDownClass(cls):
        '''
        stop service
        '''
        cherrypy.server.stop()
        cherrypy.engine.stop()
        cherrypy.engine.exit()

    def setUp(self):
        '''
        setup - remember the service URL
        '''
        self.url = 'http://%s:%s%s' % (
            cherrypy.config['server.socket_host'],
            cherrypy.config['server.socket_port'],
            mmshop.API_URL)

    def webapp_request(self, path='/', method='GET', data=None, header=None,
                       **kwargs):
        '''
        Make a HTTP request to the service.
        :param path: The path to be accessed
        :param method: The HTTP method (default ´GET´)
        :param data: data to be sent with the request
        :param header: header information to be sent with the request
        :return: The HTTP response
        '''
        req = urllib.request.Request(self.url + path)
        req_data = None
        if data is not None:
            if isinstance(data, dict):
                req.add_header('Content-Type',
                               'application/json; charset=utf-8')
                req_data = json.dumps(data)
            else:
                req.add_header('Content-Type',
                               'application/text; charset=utf-8')
                req_data = str(data)
            req_data = req_data.encode('utf-8')
            req.add_header('Content-Length', len(req_data))
        if method:
            req.method = method.upper()
        if header:
            for k, v in header:
                req.add_header(k, v)
        try:
            response = urllib.request.urlopen(req, data=req_data)
        except Exception as e:
            raise e
        return response


class TestMickeyMouseShop(_TestWebApp):
    '''
    Basic test  for items service
    '''
    def test_001_item_all(self):
        response = self.webapp_request('/item')
        # status
        got = response.status
        exp = 200
        self.assertTrue(got == exp, 'bad status: %s' % response.status)
        # data
        data = json.loads(response.read().decode())
        got = len(data)
        exp = 3
        self.assertTrue(got == exp,
                        'items count wrong: %s :: %s' % (got, exp))

    def test_002_item_by_id(self):
        response = self.webapp_request('/item/0')
        # status
        got = response.status
        exp = 200
        self.assertTrue(got == exp, 'bad status: %s' % response.status)
        # data
        data = json.loads(response.read().decode())
        got = data
        exp = {'id': 0, 'name': 'cheese', 'price': 2.63}
        self.assertTrue(got == exp,
                        'item data wrong: %s :: %s' % (got, exp))

    def test_003_item_new(self):
        item_new = {'name': 'banana', 'price': 0.29}
        response = self.webapp_request('/item', method='POST', data=item_new)
        # status
        got = response.status
        exp = 201
        self.assertTrue(got == exp, 'bad status: %s' % response.status)
        # data
        data = json.loads(response.read().decode())
        got = data
        exp = dict(item_new)
        exp['id'] = 3
        self.assertTrue(got == exp,
                        'item data wrong: %s :: %s' % (got, exp))

    def test_004_item_update(self):
        item_upd = {'name': 'mouse', 'price': 10.99}
        response = self.webapp_request('/item/3', method='PUT', data=item_upd)
        # status
        got = response.status
        exp = 200
        self.assertTrue(got == exp, 'bad status: %s' % response.status)
        # data
        data = json.loads(response.read().decode())
        got = data
        exp = dict(item_upd)
        exp['id'] = 3
        self.assertTrue(got == exp,
                        'item data wrong: %s :: %s' % (got, exp))

    def test_006_stats(self):
        response = self.webapp_request('/stats')
        # status
        got = response.status
        exp = 200
        self.assertTrue(got == exp, 'bad status: %s' % response.status)
        # data
        data = json.loads(response.read().decode())
        got = data
        exp = {'items_count': 4,
               'items_value': 18.28}
        self.assertTrue(got == exp,
                        'stats wrong: got[%s] :: exp[%s]' % (got, exp))


if __name__ == "__main__":
    # :note: ignore warnings from cheroot
    # :todo: there are some errors by shutting down the server and engine
    unittest.main(warnings='ignore')
