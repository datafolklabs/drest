"""Tests for drest.resource."""

import os
import re
import unittest
import copy
from random import random
from nose.tools import eq_, ok_, raises

import drest
from drest.testing import MOCKAPI

class ResourceTestCase(unittest.TestCase):
    def test_rest_get_all(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users')
        response = api.users.get()
        eq_(response.data['objects'][0]['username'], 'admin')

    def test_rest_get_one(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users')
        response = api.users.get(2)
        eq_(response.data['username'], 'john.doe')

    @raises(drest.exc.dRestRequestError)
    def test_rest_get_one_bad(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users', path='/bogus_path/')
        try:
            response = api.users.get(1)
        except drest.exc.dRestRequestError as e:
            eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
            raise

    def test_rest_post(self):
        api = drest.api.TastyPieAPI(MOCKAPI)
        api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
        rand_label = "Test Project %s" % random()
        response = api.projects.post(dict(label=rand_label))
        ok_(response.status, 200)

        m = re.match('http://(.*):8000\/api\/v0\/(.*)\/', 
                     response.headers['location'])
        ok_(m)

    @raises(drest.exc.dRestRequestError)
    def test_rest_post_bad(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users', path='/bogus_path/')
        try:
            response = api.users.post({})
        except drest.exc.dRestRequestError as e:
            eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users)')
            raise
        
    def test_rest_create(self):
        api = drest.api.TastyPieAPI(MOCKAPI)
        api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
        rand_label = "Test Project %s" % random()
        response = api.projects.create(dict(label=rand_label))
        ok_(response.status, 200)

    def test_rest_put(self):
        rand_label = "Test Project %s" % random()
        api = drest.api.TastyPieAPI(MOCKAPI)
        response = api.projects.get(1)

        response.data['label'] = rand_label
        response = api.projects.put(1, response.data)
    
        response = api.projects.get(1)
        eq_(response.data['label'], rand_label)

    @raises(drest.exc.dRestRequestError)
    def test_rest_put_bad(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users', path='/bogus_path/')
        try:
            response = api.users.put(1)
        except drest.exc.dRestRequestError as e:
            eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
            raise
        
    def test_rest_update(self):
        rand_label = "Test Project %s" % random()
        api = drest.api.TastyPieAPI(MOCKAPI)
        response = api.projects.get(1)

        response.data['label'] = rand_label
        response = api.projects.update(1, response.data)
    
        response = api.projects.get(1)
        eq_(response.data['label'], rand_label)

    def test_rest_patch(self):
        rand_label = "Test Project %s" % random()
        api = drest.api.TastyPieAPI(MOCKAPI)
        response = api.projects.get(1)

        new_data = dict()
        new_data['label'] = rand_label
        response = api.projects.patch(1, new_data)
        eq_(response.status, 202)
        
        response = api.projects.get(1)
        eq_(response.data['label'], rand_label)
        
        
    @raises(drest.exc.dRestRequestError)
    def test_rest_patch_bad(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users', path='/bogus_path/')
        try:
            response = api.users.patch(1)
        except drest.exc.dRestRequestError as e:
            eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 1)')
            raise
            
    def test_rest_delete(self):
        api = drest.api.TastyPieAPI(MOCKAPI)
        rand_label = "Test Project %s" % random()
    
        response = api.projects.create(dict(label=rand_label))
        ok_(response.status, 200)
    
        response = api.projects.get(params=dict(label__exact=rand_label))
        response = api.projects.delete(response.data['objects'][0]['id'])
        eq_(response.status, 204)

    @raises(drest.exc.dRestRequestError)
    def test_rest_delete_bad(self):
        api = drest.api.API(MOCKAPI)
        api.add_resource('users', path='/bogus_path/')
        try:
            response = api.users.delete(100123123)
        except drest.exc.dRestRequestError as e:
            eq_(e.msg, 'Received HTTP Code 404 - Not Found (resource: users, id: 100123123)')
            raise

    def test_tastypie_resource_handler(self):
        api = drest.api.TastyPieAPI(MOCKAPI)
        api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
        response = api.users.get_by_uri('/api/v0/users/1/')
        eq_(response.data['username'], 'admin')

    def test_tastypie_schema(self):
        api = drest.api.TastyPieAPI(MOCKAPI)
        eq_(api.users.schema['allowed_list_http_methods'], ['get'])

    def test_tastypie_patch_list(self):
        api = drest.api.TastyPieAPI(MOCKAPI)
        api.auth(user='john.doe', api_key='JOHNDOE_API_KEY')
        # Test Creating:
        new_project1 = dict(
            update_date='2013-02-27T21:07:26.403343',
            create_date='2013-02-27T21:07:26.403323',
            label='NewProject1'
            )

        new_project2 = dict(
            update_date='2013-02-27T21:07:27.403343',
            create_date='2013-02-27T21:07:27.403323',
            label='NewProject2'
            )

        response = api.projects.patch_list([new_project1, new_project2])
        eq_(response.status, 202)
        
        projects = api.projects.get().data['objects']
        labels = [p['label'] for p in projects]
        
        res = new_project1['label'] in labels
        ok_(res)
        
        res = new_project2['label'] in labels
        ok_(res)
        
        new_labels = ['NewProject1', 'NewProject2']
        new_uris = [p['resource_uri'] for p in projects \
                                      if p['label'] in new_labels]
        
        # Test Deleting:
        response = api.projects.patch_list([], new_uris)
        eq_(response.status, 202)
        
        projects = api.projects.get().data['objects']
        labels = [p['label'] for p in projects]
        
        res = 'NewProject1' not in labels
        ok_(res)
        
        res = 'NewProject2' not in labels
        ok_(res)
