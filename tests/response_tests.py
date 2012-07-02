"""Tests for drest.response."""

import os
import unittest
from nose.tools import ok_, eq_, raises

import drest
from drest.testing import MOCKAPI

api = drest.api.TastyPieAPI(MOCKAPI)

class ResponseTestCase(unittest.TestCase):
    def test_good_status(self):
        response = api.users.get()
        eq_(response.status, 200)
    
    @raises(drest.exc.dRestRequestError)
    def test_bad_status(self):
        try:
            response = api.users.get(132412341)
        except drest.exc.dRestRequestError as e:
            eq_(e.response.status, 404)
            raise
    