"""Tests for drest.api."""

import os
from nose.tools import ok_, eq_, raises

import drest
from drest.testing import MOCKAPI

api = drest.api.API(MOCKAPI)

class MyAPI(drest.api.TastyPieAPI):
    class Meta:
        baseurl = MOCKAPI
        extra_headers = dict(foo='bar')
        extra_params = dict(foo2='bar2')
        extra_url_params = dict(foo3='bar3')
        
def test_auth():
    api.auth('john.doe', 'password')
    eq_(api.request._auth_credentials[0], 'john.doe')
    eq_(api.request._auth_credentials[1], 'password')
    
def test_custom_auth():
    class MyAPI(drest.API):
        def auth(self, *args, **kw):
            for key in kw:
                self.request.add_url_param(key, kw[key])
    myapi = MyAPI(MOCKAPI)
    myapi.auth(user='john.doe', password='password')
    eq_(myapi.request._extra_url_params['user'], 'john.doe')
    eq_(myapi.request._extra_url_params['password'], 'password')
    
def test_extra_headers():
    api = MyAPI()
    eq_('bar', api.request._extra_headers['foo'])
    
def test_extra_params():
    api = MyAPI()
    eq_('bar2', api.request._extra_params['foo2'])
    
def test_extra_url_params():
    api = MyAPI()
    eq_('bar3', api.request._extra_url_params['foo3'])
    
def test_request():
    response, data = api.make_request('GET', '/')
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
    eq_(api.request._extra_headers, 
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

    eq_(api.request._auth_credentials[0], 'john.doe')
    eq_(api.request._auth_credentials[1], 'password')
    
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
