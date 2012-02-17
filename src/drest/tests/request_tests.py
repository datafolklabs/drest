"""Tests for drest.request."""

import os
import json
from random import random
from nose.tools import eq_, raises

import drest
from drest.testing import MOCKAPI

def test_debug():
    os.environ['DREST_DEBUG'] = '1'
    req = drest.request.RequestHandler(baseurl=MOCKAPI, debug=True)
    req.request('GET', '/')
    eq_(req._meta.debug, True)
    os.environ['DREST_DEBUG'] = '0'

def test_no_serialization():
    req = drest.request.RequestHandler(baseurl=MOCKAPI, serialization=False)
    response, data = req.request('GET', '/users/1/')
    eq_(json.loads(data.decode('utf-8'))['username'], 'admin')

@raises(drest.exc.dRestAPIError)
def test_socket_error():
    req = drest.request.RequestHandler(baseurl='http://localhost/bogus/api')
    try:
        response, data = req.request('GET', '/users/1/')
    except drest.exc.dRestAPIError as e:
        eq_(e.msg, 'Connection refused')
        raise
        
def test_extra_params():
    params = {}
    params['label'] = "Project Label %s" % random()
    req = drest.request.TastyPieRequestHandler(baseurl=MOCKAPI)
    req.add_param('label', params['label'])
    eq_(req._extra_params, params)
    response, data = req.request('POST', '/projects/', params)

def test_extra_url_params():
    req = drest.request.RequestHandler(baseurl=MOCKAPI)
    req.add_url_param('username__icontains', 'ad')
    eq_(req._extra_url_params, dict(username__icontains='ad'))
    response, data = req.request('GET', '/users/')
    eq_(data['objects'][0]['username'], 'admin')
    
    
def test_extra_headers():
    req = drest.request.RequestHandler(baseurl=MOCKAPI, serialization=False)
    req.add_header('some_key', 'some_value')
    eq_(req._extra_headers, dict(some_key='some_value'))
    response, data = req.request('GET', '/users/')
    
@raises(drest.exc.dRestRequestError)
def test_handle_response():
    req = drest.request.RequestHandler(baseurl=MOCKAPI)
    response, data = req.request('GET', '/users/1/')
    response.status = 404
    try:
        req.handle_response(response, {})
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found')
        raise

def test_ignore_ssl_validation():
    req = drest.request.RequestHandler(baseurl=MOCKAPI, serialization=False, 
                                       ignore_ssl_validation=True)
    req.request('GET', '/users/')
    