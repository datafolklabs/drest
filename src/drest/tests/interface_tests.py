"""Tests for drest.interface."""

import os
import unittest
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
     
class InterfaceTestCase(unittest.TestCase):
    @raises(drest.exc.dRestInterfaceError)
    def test_interface(self):
        _int = drest.interface.Interface()

    def test_attribute(self):
        attr = drest.interface.Attribute('Attr Description')
        eq_(str(attr), 'Attribute: Attr Description')

    def test_validate(self):
        drest.interface.validate(ITest, TestHandler(), ['test_func'])

    def test_validate_meta(self):
        drest.interface.validate(ITest, TestHandler(), ['test_func'], ['test_meta'])

    @raises(drest.exc.dRestInterfaceError)
    def test_validate_missing_member(self):
        try:
            drest.interface.validate(ITest, TestHandler(), ['missing_func'])
        except drest.exc.dRestInterfaceError as e:
            eq_(e.msg, "Invalid or missing: ['missing_func'] in TestHandler")
            raise

    @raises(drest.exc.dRestInterfaceError)
    def test_validate_missing_meta(self):
        try:
            drest.interface.validate(ITest, TestHandler(), [], ['missing_meta'])
        except drest.exc.dRestInterfaceError as e:
            eq_(e.msg, "Invalid or missing: ['_meta.missing_meta'] in TestHandler")
            raise