"""Tests for drest.request."""

import os
import unittest
from random import random
from nose.tools import eq_, raises

try:
    import json
except ImportError as e:
    import simplejson as json
        
import drest
from drest.testing import MOCKAPI

class RequestTestCase(unittest.TestCase):
    def test_debug(self):
        os.environ['DREST_DEBUG'] = '1'
        req = drest.request.RequestHandler(debug=True)
        req.make_request('GET', '%s/' % MOCKAPI)
        eq_(req._meta.debug, True)
        os.environ['DREST_DEBUG'] = '0'

    def test_no_serialization(self):
        req = drest.request.RequestHandler(serialization_handler=None)
        response = req.make_request('GET', '%s/users/1/' % MOCKAPI)
        eq_(response.data, req._deserialize(response.data))
        eq_(dict(foo='bar'), req._serialize(dict(foo='bar')))
        eq_(json.loads(response.data.decode('utf-8'))['username'], 'admin')

    @raises(drest.exc.dRestAPIError)
    def test_socket_error(self):
        req = drest.request.RequestHandler()
        try:
            response = req.make_request('GET', 'http://localhost/bogus/')
        except drest.exc.dRestAPIError as e:
            eq_(e.msg, 'Connection refused')
            raise
    
    @raises(drest.exc.dRestAPIError)
    def test_server_not_found_error(self):
        req = drest.request.RequestHandler()
        try:
            response = req.make_request('GET', 'http://bogus.example.com/api/')
        except drest.exc.dRestAPIError as e:
            eq_(e.msg, 'Unable to find the server at bogus.example.com')
            raise
        
    def test_trailing_slash(self):
        req = drest.request.RequestHandler(trailing_slash=False)
        response = req.make_request('GET', '%s/users/1/' % MOCKAPI)
    
    def test_extra_params(self):
        params = {}
        params['label'] = "Project Label %s" % random()
        req = drest.request.TastyPieRequestHandler()
        req.add_param('label', params['label'])
        eq_(req._extra_params, params)
        response = req.make_request('POST', '%s/projects/' % MOCKAPI, params)

    def test_extra_url_params(self):
        req = drest.request.RequestHandler()
        req.add_url_param('username__icontains', 'ad')
        eq_(req._extra_url_params, dict(username__icontains='ad'))
        response = req.make_request('GET', '%s/users/' % MOCKAPI)
        eq_(response.data['objects'][0]['username'], 'admin')
    
    
    def test_extra_headers(self):
        req = drest.request.RequestHandler(serialization_handler=None)
        req.add_header('some_key', 'some_value')
        eq_(req._extra_headers, dict(some_key='some_value'))
        response = req.make_request('GET', '%s/users/' % MOCKAPI)
    
    @raises(drest.exc.dRestRequestError)
    def test_handle_response(self):
        req = drest.request.RequestHandler()
        response = req.make_request('GET', '%s/users/1/' % MOCKAPI)
        response.status = 404
        try:
            req.handle_response(response)
        except drest.exc.dRestRequestError as e:
            eq_(e.msg, 'Received HTTP Code 404 - Not Found')
            raise

    def test_ignore_ssl_validation(self):
        req = drest.request.RequestHandler(serialization_handler=None, 
                                           ignore_ssl_validation=True)
        req.make_request('GET', '%s/users/' % MOCKAPI)
    