"""Tests for drest.resource."""

import os
import json
from nose.tools import eq_, raises

import drest
    
API_URL = os.environ.get('DREST_TEST_API', 'http://localhost:5000/')
GET_ALL = {
    'action': 'get_all', 
    'objects': [
            {
                'username': 'admin', 
                'id': '1'
            }, 
            {
                'username': 'john.doe', 
                'id': '2'
            }
        ], 
        'method': 'GET'
    }

GET_ONE = {
    'username': 'admin', 
    'action': 'get_one', 
    'id': '1', 
    'method': 'GET'
    }
    
def test_rest_get_all():
    api = drest.api.API(API_URL)
    api.add_resource('users')
    response, data = api.users.get()
    eq_(data, GET_ALL)

def test_rest_get_one():
    api = drest.api.API(API_URL)
    api.add_resource('users')
    response, data = api.users.get(1)
    eq_(data, GET_ONE)

@raises(drest.exc.dRestRequestError)
def test_rest_get_one_bad():
    api = drest.api.API(API_URL)
    api.add_resource('users', path='/bogus_path/')
    try:
        response, data = api.users.get(1)
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
        raise

def test_rest_post():
    api = drest.api.API(API_URL)
    api.add_resource('users')
    response, data = api.users.post({})
    eq_(data['method'], 'POST')

@raises(drest.exc.dRestRequestError)
def test_rest_post_bad():
    api = drest.api.API(API_URL)
    api.add_resource('users', path='/bogus_path/')
    try:
        response, data = api.users.post({})
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users)')
        raise
        
def test_rest_create():
    api = drest.api.API(API_URL)
    api.add_resource('users')
    response, data = api.users.create({})
    eq_(data['method'], 'POST')

def test_rest_put():
    api = drest.api.API(API_URL)
    api.add_resource('users')
    response, data = api.users.put(1, {})
    eq_(data['method'], 'PUT')

@raises(drest.exc.dRestRequestError)
def test_rest_put_bad():
    api = drest.api.API(API_URL)
    api.add_resource('users', path='/bogus_path/')
    try:
        response, data = api.users.put(1)
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
        raise
        
def test_rest_update():
    api = drest.api.API(API_URL)
    api.add_resource('users')
    response, data = api.users.update(1, {})
    eq_(data['method'], 'PUT')


def test_rest_delete():
    api = drest.api.API(API_URL)
    api._request._meta.debug = True
    api.add_resource('users', path='/users/')
    response, data = api.users.delete(1)
    eq_(data['method'], 'DELETE')

@raises(drest.exc.dRestRequestError)
def test_rest_delete_bad():
    api = drest.api.API(API_URL)
    api.add_resource('users', path='/bogus_path/')
    try:
        response, data = api.users.delete(100123123)
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 100123123)')
        raise

def test_tastypie_resource_handler():
    api = drest.api.TastyPieAPI(API_URL)
    response, data = api.users.get_by_uri('/api/v1/users/1/')
    eq_(data, {'username': 'admin', 'action': 'get_one', 'id': '1', 'method': 'GET'})

def test_tastypie_schema():
    api = drest.api.TastyPieAPI(API_URL)
    eq_(api.users.schema['action'], 'schema')

def test_resource_request_uninstantiated():
    res = drest.resource.ResourceHandler(baseurl=API_URL, 
                                         name='test', 
                                         path='/test/', 
                                         request=drest.request.RequestHandler)
    
    