#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mmshop.api
'''
:author:  madkote
:contact: madkote(at)bluewin.ch

API
---
The API implementation
'''

import cherrypy
import datetime
import jinja2
import json
import logging

import mmshop

VERSION = (0, 2, 0)

__all__ = ['MickeyMouseShop']
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)

# =============================================================================
# SETTINGS
# =============================================================================
_DEBUG = mmshop.API_FLAG_DEBUG
_PATH_WWW = mmshop.API_PATH_WWW

EXPIRE_FORMAT = '%Y%m%d%H%M'


# =============================================================================
# DUMMY
# =============================================================================
_ITEMS = [
    {
        'id': 0,
        'name': 'cheese',
        'price': 2.63,
        'expire': '201612011545'
    },
    {
        'id': 1,
        'name': 'milk',
        'price': 1.25,
        'expire': '201712011545'
    },
    {
        'id': 2,
        'name': 'chocolate',
        'price': 3.41,
        'expire': '201812011545'
    },
]


# =============================================================================
# SERVICE
# =============================================================================
class MickeyMouseShop(object):
    '''
    Simple web service API
    '''
    def __init__(self, with_index=False):
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(_PATH_WWW))  # @IgnorePep8
        self.__with_index = with_index

    def _check_item(self, _item):
        '''
        Check / validate item
        :param _item: Item to be validated
        :return: the validated item
        :raise cherrypy.HTTPError: ´404´ if item is not valid
        '''
        # ID
        if 'id' not in _item:
            raise cherrypy.HTTPError(404, 'ID field in the entity must be defined')  # @IgnorePep8
        elif isinstance(_item['id'], str):
            try:
                _item['id'] = int(_item['id'])
            except Exception as e:
                raise cherrypy.HTTPError(404, 'ID field in the entity must be integer: %s' % e)  # @IgnorePep8
        elif not isinstance(_item['id'], int):
            raise cherrypy.HTTPError(404, 'ID field in the entity must be integer')  # @IgnorePep8
        # name
        if 'name' not in _item:
            raise cherrypy.HTTPError(404, 'Name field in the entity must be defined')  # @IgnorePep8
        elif not isinstance(_item['name'], str):
            try:
                _item['name'] = str(_item['name'])
            except Exception as e:
                raise cherrypy.HTTPError(404, 'Name field in the entity must be string: %s' % e)  # @IgnorePep8
        # price
        if 'price' not in _item:
            raise cherrypy.HTTPError(404, 'Price field in the entity must be defined')  # @IgnorePep8
        elif isinstance(_item['price'], str):
            try:
                _item['price'] = float(_item['price'])
            except Exception as e:
                raise cherrypy.HTTPError(404, 'ID field in the entity must be float: %s' % e)  # @IgnorePep8
        elif not isinstance(_item['price'], float):
            raise cherrypy.HTTPError(404, 'Price field in the entity must be float')  # @IgnorePep8
        # OK
        return _item

    def _GET_item(self, _id, _request):
        '''
        Get item or items list if item ID is not given
        :param _id: The item ID
        :param _request: The request
        :return: The item or items list if item ID is not given
        :raise cherrypy.HTTPError: ´404´ if item ID is invalid or
            there is no item with the given ID
        '''
        if _id is None:
            # all items
            return _ITEMS[:]
        else:
            # search for item with given ID
            try:
                _id = int(_id)
            except ValueError as e:
                raise cherrypy.HTTPError(404, 'Item ID not valid: %s' % e)
            else:
                for i in _ITEMS:
                    if i['id'] == _id:
                        return i
                else:
                    raise cherrypy.HTTPError(404, 'Item could not be found.')

    def _POST_item(self, _id, _request):
        '''
        Add new item
        :param _id: The item ID - should be empty
        :param _request: The request
        :return: The new item. Repsonse status is set to ´201´.
        :raise cherrypy.HTTPError: ´404´ if any problems processing data or
            ´409´ if the an item with same ID exists already.
        '''
        # data
        try:
            data = dict(json.loads(_request.body.read().decode("utf-8")))
        except Exception as e:
            raise cherrypy.HTTPError(404, 'Can not process data: %s' % e)
        # determine ID
        if 'id' in data:
            # existing item
            try:
                i = self._GET_item(data['id'], _request)
            except Exception as e:
                pass
            else:
                raise cherrypy.HTTPError(409, 'Item with id "%s" exists already' % data['id'])  # @IgnorePep8
        else:
            # next ID for item
            try:
                data['id'] = max([i['id'] for i in _ITEMS]) + 1
            except Exception as e:
                raise cherrypy.HTTPError(404, 'Can not find next ID: %s' % e)
        # check and add data
        try:
            data = self._check_item(data)
            _ITEMS.append(data)
        except cherrypy.HTTPError as e:
            raise e
        except Exception as e:
            raise cherrypy.HTTPError(404, 'Can not add data: %s' % e)
        else:
            cherrypy.response.status = 201
        # result
        return data

    def _PUT_item(self, _id, _request):
        '''
        Update the item by ID
        :param _id: The item ID
        :param _request: The request
        :return: Updated item
        :raise cherrypy.HTTPError: ´204´ if cannot process data or
            ´404´ if cannot update.
        '''
        # update
        try:
            data = dict(json.loads(_request.body.read().decode("utf-8")))
        except Exception as e:
            raise cherrypy.HTTPError(204, 'Can not process data: %s' % e)
        else:
            if not data:
                raise cherrypy.HTTPError(204, 'No data: %s' % e)
        try:
            # get item
            c = self._GET_item(_id, _request)
            # check if update will not break anything
            d = dict(c)
            d.update(data)
            self._check_item(d)
            # update
            c.update(data)
        except cherrypy.HTTPError as e:
            raise e
        except Exception as e:
            raise cherrypy.HTTPError(404, 'Cannot update data: %s' % e)
        return c

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get'])
    def index(self):
        '''
        Index page: overview of all available items
        '''
        if not self.__with_index:
            raise cherrypy.HTTPError(404,
                                     'The path "%s" was not found.' %
                                     mmshop.API_URL)
        tmpl = self.env.get_template('mmshop.html')
        data = {'title': 'Welcome to Mickey Mouse shop',
                'items': self._GET_item(None, cherrypy.request),
                'expire': {},
                'rest_api_version': mmshop.__version__}
        now = datetime.datetime.now()
        for item in data['items']:
            if 'expire' in item:
                item_now = datetime.datetime.strptime(item['expire'],
                                                      EXPIRE_FORMAT)
                data['expire'][item['id']] = now >= item_now
            else:
                data['expire'][item['id']] = True
        return tmpl.render(**data)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get', 'post', 'put'])
    @cherrypy.config(**{'tools.json_out.on': True})
    def item(self, item_id=None):
        '''
        Item operations:
        - GET  :: an item by ID or all items if no ID specified
        - POST :: add new item
        - PUT  :: update an item
        :param item_id: The item ID (optionally)
        :return: Item or item list
        '''
        # info
        if _DEBUG:
            logging.debug('')
            logging.debug('*' * 50)
            logging.debug('* %s' % cherrypy.request.method)
            logging.debug('* %s <%s>' % (item_id, type(item_id)))
        # process request
        if cherrypy.request.method == 'GET':
            res = self._GET_item(item_id, cherrypy.request)
        elif cherrypy.request.method == 'POST':
            res = self._POST_item(item_id, cherrypy.request)
        elif cherrypy.request.method == 'PUT':
            res = self._PUT_item(item_id, cherrypy.request)
        else:
            raise cherrypy.HTTPError(405, 'Method %s is not allowed' % cherrypy.request.method)  # @IgnorePep8
        if _DEBUG:
            logging.debug('* %s' % res)
            logging.debug('*' * 50)
            logging.debug('')
        return res

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['get'])
    @cherrypy.config(**{'tools.json_out.on': True})
    def stats(self):
        '''
        Get basic statistics like count of items and their value
        :return: The statistics
        '''
        return {'items_count': len(_ITEMS),
                'items_value': sum([i['price'] for i in _ITEMS])}
