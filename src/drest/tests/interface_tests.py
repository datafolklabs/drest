"""Tests for drest.interface."""

import os
from nose.tools import eq_, raises
import drest
from drest.testing import MOCKAPI

api = drest.api.API(MOCKAPI)

class ITest(drest.interface.Interface):
    pass

class TestHandler(drest.meta.MetaMixin):
    class Meta:
        test_meta = 'some value'
        
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

def test_validate():
    drest.interface.validate(ITest, TestHandler(), ['test_func'])

def test_validate_meta():
    drest.interface.validate(ITest, TestHandler(), ['test_func'], ['test_meta'])

@raises(drest.exc.dRestInterfaceError)
def test_validate_missing_member():
    try:
        drest.interface.validate(ITest, TestHandler(), ['missing_func'])
    except drest.exc.dRestInterfaceError as e:
        eq_(e.msg, "Invalid or missing: ['missing_func'] in TestHandler")
        raise

@raises(drest.exc.dRestInterfaceError)
def test_validate_missing_meta():
    try:
        drest.interface.validate(ITest, TestHandler(), [], ['missing_meta'])
    except drest.exc.dRestInterfaceError as e:
        eq_(e.msg, "Invalid or missing: ['_meta.missing_meta'] in TestHandler")
        raise