"""Tests for drest.request."""

import os
import unittest
import mock
from random import random
from nose.tools import eq_, ok_, raises

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
            response = req.make_request('GET', 'http://bogusurl.localhost/')
        except drest.exc.dRestAPIError as e:
            res = e.__repr__().find('Unable to find the server')
            test_res = res >= 0
            ok_(test_res)
            raise

    @raises(drest.exc.dRestAPIError)
    def test_socket_timeout(self):
        req = drest.request.RequestHandler(timeout=1)
        try:
            response = req.make_request(
                'GET',
                'http://localhost:8000/fake_long_request/',
                params=dict(seconds=10),
                )
        except drest.exc.dRestAPIError as e:
            res = e.__repr__().find('timed out')
            test_res = res >= 0
            ok_(test_res)
            raise

    @raises(drest.exc.dRestAPIError)
    def test_server_not_found_error(self):
        req = drest.request.RequestHandler()
        try:
            response = req.make_request('GET', 'http://bogus.example.com/api/')
        except drest.exc.dRestAPIError as e:
            res = e.__repr__().find('Unable to find the server')
            test_res = res >= 0
            ok_(test_res)
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

    def test_payload_and_headers_are_none(self):
        req = drest.request.TastyPieRequestHandler()
        response = req._make_request('%s/projects/' % MOCKAPI, 'GET',
                                     payload=None, headers=None)

        req = drest.request.TastyPieRequestHandler(serialize=False)
        response = req._make_request('%s/projects/' % MOCKAPI, 'GET',
                                     payload=None, headers=None)

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

    def test_get_request_allow_get_body(self):
        # lighttpd denies GET requests with data in the body by default
        class MyRequestHandler(drest.request.RequestHandler):
            class Meta:
                allow_get_body = False

        request = MyRequestHandler()
        request._get_http = mock.Mock()
        request._get_http().request.return_value = ({'status': 200}, '')
        url = '%s/users/' % MOCKAPI
        request.make_request('GET', url, {"param1": "value1"})
        headers = {'Content-Type': 'application/json'}

        url = url + '?param1=value1'
        request._get_http()\
               .request.assert_called_with(url, 'GET', '', headers=headers)
