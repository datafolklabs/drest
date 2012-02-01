"""Tests for drest.serialization."""

import os
import json
from nose.tools import eq_, raises
import drest
    
API_URL = os.environ.get('DREST_TEST_API', 'http://localhost:5000/')

def test_serialization():
    s = drest.serialization.SerializationHandler()
    s.get_headers()
    
@raises(NotImplementedError)
def test_serialization_serialize():
    s = drest.serialization.SerializationHandler()
    s.get_headers()
    s.serialize({})

@raises(NotImplementedError)
def test_serialization_deserialize():
    s = drest.serialization.SerializationHandler()
    s.get_headers()
    s.deserialize(json.dumps({}))
    
