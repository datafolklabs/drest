
from . import interface, exc, meta

def validate(obj):
    """Validates a handler implementation against the ISerialize interface."""
    members = [
        'serialize',
        'deserialize',
        'get_headers',
        ]
    interface.validate(ISerialization, obj, members)
    
class ISerialization(interface.Interface):
    """
    This class defines the Serialization Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    All implementations must provide sane 'default' functionality when 
    instantiated with no arguments.  Meaning, it can and should accept 
    optional parameters that alter how it functions, but can not require
    any parameters.  
    
    Implementations do *not* subclass from interfaces.
            
    """

    def get_headers():
        """
        Return a dictionary of additional headers to include in requests.
        
        """
        
    def deserialize():
        """
        Load a serialized string and return a dictionary of key/value pairs.
        
        Required Arguments:
        
            serialized_data
                A string of serialzed data.
        
        Returns: dict
        
        """
        
    def serialize():
        """
        Dump a dictionary of values from a serialized string.
        
        Required Arguments:
                                
            data_dict
                A data dictionary to serialize.

        Returns: string
        
        """
        
class SerializationHandler(meta.MetaMixin):
    """
    Generic Serialization Handler.  Should be used to subclass from.
            
    """
    def __init__(self, **kw):
        super(SerializationHandler, self).__init__(**kw)
        
    def get_headers(self):
        return {}
        
    def deserialize(self, serialized_string):
        raise NotImplementedError
    
    def serialize(self, dict_obj):
        raise NotImplementedError
        

class JsonSerializationHandler(SerializationHandler):
    """
    This handler implements the ISerialization interface using the standard 
    json library.
    
    """
    def __init__(self, **kw):
        try:
            import json # pragma: no cover
        except ImportError as e: # pragma: no cover
            import simplejson as json # pragma: no cover
            
        self.backend = json
        super(JsonSerializationHandler, self).__init__(**kw)
        
    def deserialize(self, serialized_string):
        try:
            # Fix for Python3
            if type(serialized_string) == bytes:
                serialized_string = serialized_string.decode('utf-8')
        
            return self.backend.loads(serialized_string)
        except ValueError as e:
            return dict(error=e.args[0])

    def serialize(self, dict_obj):
        return self.backend.dumps(dict_obj)
                
    def get_headers(self):
        headers = {
            'Content-Type' : 'application/json',
            }
        return headers
