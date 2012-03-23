"""Tests for drest.resource."""

import os
from random import random
from nose.tools import eq_, ok_, raises

import drest
from drest.testing import MOCKAPI

def test_rest_get_all():
    api = drest.api.API(MOCKAPI)
    api.add_resource('users')
    response = api.users.get()
    eq_(response.data['objects'][0]['username'], 'admin')

def test_rest_get_one():
    api = drest.api.API(MOCKAPI)
    api.add_resource('users')
    response = api.users.get(2)
    eq_(response.data['username'], 'john.doe')

@raises(drest.exc.dRestRequestError)
def test_rest_get_one_bad():
    api = drest.api.API(MOCKAPI)
    api.add_resource('users', path='/bogus_path/')
    try:
        response = api.users.get(1)
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
        raise

def test_rest_post():
    api = drest.api.TastyPieAPI(MOCKAPI)
    api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
    rand_label = "Test Project %s" % random()
    response = api.projects.post(dict(label=rand_label))
    ok_(response.status, 200)

@raises(drest.exc.dRestRequestError)
def test_rest_post_bad():
    api = drest.api.API(MOCKAPI)
    api.add_resource('users', path='/bogus_path/')
    try:
        response = api.users.post({})
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users)')
        raise
        
def test_rest_create():
    api = drest.api.TastyPieAPI(MOCKAPI)
    api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
    rand_label = "Test Project %s" % random()
    response = api.projects.create(dict(label=rand_label))
    ok_(response.status, 200)

def test_rest_put():
    rand_label = "Test Project %s" % random()
    api = drest.api.TastyPieAPI(MOCKAPI)
    response = api.projects.get(1)

    response.data['label'] = rand_label
    response = api.projects.put(1, response.data)
    
    response = api.projects.get(1)
    eq_(response.data['label'], rand_label)

@raises(drest.exc.dRestRequestError)
def test_rest_put_bad():
    api = drest.api.API(MOCKAPI)
    api.add_resource('users', path='/bogus_path/')
    try:
        response = api.users.put(1)
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
        raise
        
def test_rest_update():
    rand_label = "Test Project %s" % random()
    api = drest.api.TastyPieAPI(MOCKAPI)
    response = api.projects.get(1)

    response.data['label'] = rand_label
    response = api.projects.update(1, response.data)
    
    response = api.projects.get(1)
    eq_(response.data['label'], rand_label)


def test_rest_delete():
    api = drest.api.TastyPieAPI(MOCKAPI)
    rand_label = "Test Project %s" % random()
    
    response = api.projects.create(dict(label=rand_label))
    ok_(response.status, 200)
    
    response = api.projects.get(params=dict(label__exact=rand_label))
    response = api.projects.delete(response.data['objects'][0]['id'])
    eq_(response.status, 204)

@raises(drest.exc.dRestRequestError)
def test_rest_delete_bad():
    api = drest.api.API(MOCKAPI)
    api.add_resource('users', path='/bogus_path/')
    try:
        response = api.users.delete(100123123)
    except drest.exc.dRestRequestError as e:
        eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 100123123)')
        raise

def test_tastypie_resource_handler():
    api = drest.api.TastyPieAPI(MOCKAPI)
    api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
    response = api.users.get_by_uri('/api/v0/users/1/')
    eq_(response.data['username'], 'admin')

def test_tastypie_schema():
    api = drest.api.TastyPieAPI(MOCKAPI)
    eq_(api.users.schema['allowed_list_http_methods'], ['get'])

