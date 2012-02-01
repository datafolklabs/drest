"""Tests for drest.request."""

import os
import json
from nose.tools import eq_, raises

import drest
    
API_URL = os.environ.get('DREST_TEST_API', 'http://localhost:5000/')

def test_debug():
    os.environ['DREST_DEBUG'] = '1'
    req = drest.request.RequestHandler(baseurl=API_URL, debug=True)
    req.request('GET', '/')
    eq_(req._meta.debug, True)
    os.environ['DREST_DEBUG'] = '0'

def test_no_serialization():
    req = drest.request.RequestHandler(baseurl=API_URL, serialization=False)
    response, data = req.request('GET', '/users/1/')
    eq_(data.decode('utf-8'), json.dumps({"username": "admin", "action": "get_one", "id": "1", "method": "GET"}))

@raises(drest.exc.dRestAPIError)
def test_socket_error():
    req = drest.request.RequestHandler(baseurl='http://localhost/bogus/api')
    try:
        response, data = req.request('GET', '/users/1/')
    except drest.exc.dRestAPIError as e:
        eq_(e.msg, 'Connection refused')
        raise
        
def test_extra_params():
    req = drest.request.RequestHandler(baseurl=API_URL)
    req.add_param('some_key', 'some_value')
    eq_(req._extra_params, dict(some_key='some_value'))
    response, data = req.request('POST', '/users/')

def test_extra_url_params():
    req = drest.request.RequestHandler(baseurl=API_URL)
    req.add_url_param('some_key', 'some_value')
    eq_(req._extra_url_params, dict(some_key='some_value'))
    response, data = req.request('POST', '/users/')
    
def test_extra_headers():
    req = drest.request.RequestHandler(baseurl=API_URL, serialization=False)
    req.add_header('some_key', 'some_value')
    eq_(req._extra_headers, dict(some_key='some_value'))
    response, data = req.request('POST', '/users/')
    
@raises(drest.exc.dRestRequestError)
def test_handle_response():
    req = drest.request.RequestHandler(baseurl=API_URL)
    response, data = req.request('GET', '/users/1/')
    response.status = 404
    try:
        req.handle_response(response, {})
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found')
        raise