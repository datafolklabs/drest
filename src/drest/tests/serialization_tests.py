"""Tests for drest.serialization."""

import os

try:
    import json
except ImportError as e:
    import simplejson as json
    
from nose.tools import eq_, raises
import drest

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
    
