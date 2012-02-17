"""Tests for drest.api."""

import os
from nose.tools import ok_, eq_, raises

import drest
from drest.testing import MOCKAPI

api = drest.api.API(MOCKAPI)

def test_auth():
    api.auth('john.doe', 'password')
    eq_(api._request._auth_credentials[0], 'john.doe')
    eq_(api._request._auth_credentials[1], 'password')
    
def test_custom_auth():
    class MyAPI(drest.API):
        def auth(self, *args, **kw):
            for key in kw:
                self._request.add_url_param(key, kw[key])
    myapi = MyAPI(MOCKAPI)
    myapi.auth(user='john.doe', password='password')
    eq_(myapi._request._extra_url_params['user'], 'john.doe')
    eq_(myapi._request._extra_url_params['password'], 'password')
    
def test_request():
    response, data = api.request('GET', '/')
    res = 'users' in data
    ok_(res)

def test_add_resource():
    api.add_resource('users')
    response, data = api.users.get()
    
    api.add_resource('users2', path='/users/')
    response, data = api.users2.get()
    
    api.add_resource('users3', path='/users/', 
                     resource_handler=drest.resource.RESTResourceHandler)
    response, data = api.users3.get()
    
@raises(drest.exc.dRestResourceError)
def test_duplicate_resource():
    api.add_resource('users')

def test_tastypieapi_via_apikey_auth():
    api = drest.api.TastyPieAPI(MOCKAPI)
    api.auth(user='john.doe', api_key='JOHN_DOE_API_KEY')
    
    # verify headers
    eq_(api._request._extra_headers, 
        {'Content-Type': 'application/json', 
         'Authorization': 'ApiKey john.doe:JOHN_DOE_API_KEY'})
    
    # verify resources
    res = 'users' in api.resources
    ok_(res)
    res = 'projects' in api.resources
    ok_(res)
    
    # and requests
    response, data = api.users_via_apikey_auth.get()
    eq_(data['objects'][0]['username'], 'admin')
    
    response, data = api.projects.get(params=dict(label__startswith='Test Project'))
    ok_(data['objects'][0]['label'].startswith('Test Project'))

def test_tastypieapi_via_basic_auth():
    api = drest.api.TastyPieAPI(MOCKAPI, auth_mech='basic')
    api.auth(user='john.doe', password='password')

    eq_(api._request._auth_credentials[0], 'john.doe')
    eq_(api._request._auth_credentials[1], 'password')
    
    # verify resources
    res = 'users' in api.resources
    ok_(res)
    res = 'projects' in api.resources
    ok_(res)
    
    # and requests
    response, data = api.users_via_basic_auth.get()
    eq_(data['objects'][0]['username'], 'admin')

@raises(drest.exc.dRestAPIError)
def test_tastypieapi_via_unknown_auth():
    api = drest.api.TastyPieAPI(MOCKAPI, auth_mech='bogus')
    api.auth(user='john.doe', password='password')
