"""Tests for drest.interface."""

import os
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

import drest

API_URL = os.environ.get('DREST_TEST_API', 'http://localhost:5000/')
api = drest.api.API(API_URL)

class ITest(drest.interface.Interface):
    pass

class TestHandler(object):
    def test_func(self):
        pass
    
    def __repr__(self):
        return 'TestHandler'
     
@raises(drest.exc.dRestInterfaceError)
def test_interface():
    _int = drest.interface.Interface()

def test_attribute():
    attr = drest.interface.Attribute('Attr Description')
    eq_(str(attr), 'Attribute: Attr Description')
    eq_(attr.__unicode__(), unicode('Attribute: Attr Description'))

def test_validate():
    drest.interface.validate(ITest, TestHandler(), ['test_func'])

@raises(drest.exc.dRestInterfaceError)
def test_validate_missing_member():
    try:
        drest.interface.validate(ITest, TestHandler(), ['missing_func'])
    except drest.exc.dRestInterfaceError as e:
        eq_(e.msg, "Invalid or missing: ['missing_func'] in TestHandler")
        raise