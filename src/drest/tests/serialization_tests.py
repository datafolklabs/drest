"""Tests for drest.serialization."""

import os
import unittest

try:
    import json
except ImportError as e:
    import simplejson as json
    
from nose.tools import eq_, raises
import drest

class SerializationTestCase(unittest.TestCase):
    def test_serialization(self):
        s = drest.serialization.SerializationHandler()
        s.get_headers()
    
    @raises(NotImplementedError)
    def test_serialization_serialize(self):
        s = drest.serialization.SerializationHandler()
        s.get_headers()
        s.serialize({})

    @raises(NotImplementedError)
    def test_serialization_deserialize(self):
        s = drest.serialization.SerializationHandler()
        s.get_headers()
        s.deserialize(json.dumps({}))
    
