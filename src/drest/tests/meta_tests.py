"""Tests for drest.meta."""

from nose.tools import eq_
import drest
    
class Test(drest.meta.MetaMixin):
    class Meta:
        some_param = None
        
    def __init__(self, **kw):
        super(Test, self).__init__(**kw)
        
def test_meta():
    test = Test(some_param='some_value')
    eq_(test._meta.some_param, 'some_value')