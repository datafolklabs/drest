"""Tests for drest.api."""

import os
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

import drest

API_URL = os.environ.get('DREST_TEST_API', 'http://localhost:5000/')
api = drest.api.API(API_URL)

def test_auth():
    api.auth(user='john.doe', password='oober-secure-password')

def test_request():
    response, data = api.request('GET', '/')
    res = 'users' in data
    ok_(res)

def test_add_resource():
    api.add_resource('users')
    response, data = api.users.get()
    eq_(data['method'], 'GET')
    eq_(data['action'], 'get_all')

    api.add_resource('users2', path='/users/')
    response, data = api.users2.get()
    eq_(data['method'], 'GET')
    eq_(data['action'], 'get_all')
    
    api.add_resource('users3', path='/users/', 
                     resource_handler=drest.resource.ResourceHandler)
    response, data = api.users3.get()
    eq_(data['method'], 'GET')
    eq_(data['action'], 'get_all')

@raises(drest.exc.dRestResourceError)
def test_duplicate_resource():
    api.add_resource('users')

def test_tastypieapi():
    api = drest.api.TastyPieAPI(API_URL)
    api.auth(user='john.doe', api_key='XXXXX')
    
    # verify headers
    eq_(api._request._extra_headers, 
        {'Content-Type': 'application/json', 
         'Authorization': 'ApiKey john.doe:XXXXX'})
    
    # verify resources
    eq_(api.resources, ['users', 'projects'])
    
    # and requests
    response, data = api.users.get()
    eq_(data['method'], 'GET')
    eq_(data['action'], 'get_all')
