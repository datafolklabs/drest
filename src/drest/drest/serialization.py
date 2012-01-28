
from drest import interface, exc, meta

def validate(klass, obj):
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
    
    Optional Arguments (Meta):
    
        backend 
            The backend to use (i.e. json, yaml, etc)
        
        serialize
            The function that serialized data on backend.
            
        deserialize
            The function that deserializes data on backend.
            
    """
    class Meta:
        backend = None
        serialize = 'dumps'
        deserialize = 'loads'
        
    def __init__(self, **kw):
        super(SerializationHandler, self).__init__(**kw)
        
    def get_headers(self):
        return {}
        
    def deserialize(self, serialized_string):
        try:
            func = getattr(self._meta.backend, self._meta.deserialize)
            return func(serialized_string.strip('\n'))
        except ValueError, e:
            return dict(error=e.args[0])
    
    def serialize(self, dict_obj):
        try:
            func = getattr(self._meta.backend, self._meta.serialize)
            return func(dict_obj)
        except ValueError, e:
            return dict(error=e.args[0])

class JsonSerializationHandler(SerializationHandler):
    """
    This handler implements the ISerialization interface using the standard 
    json library.
    
    """
    def __init__(self, **kw):
        import json
        
        kw['backend'] = kw.get('backend', json)
        super(JsonSerializationHandler, self).__init__(**kw)
        
    def get_headers(self):
        headers = {
            'Content-Type' : 'application/json',
            }
        return headers
        
class YamlSerializationHandler(SerializationHandler):
    """
    This handler implements the ISerialization interface using the yaml 
    library.
    
    """
    
    def __init__(self, **kw):
        import yaml
        
        kw['backend'] = kw.get('backend', yaml)
        kw['backend'] = kw.get('serialize', 'dump')
        super(YamlSerializationHandler, self).__init__(**kw)
        
    def get_headers(self):
        headers = {
            'Content-Type' : 'application/yaml',
            }
        return headers
        