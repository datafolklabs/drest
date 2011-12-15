
from drest import interface, exc

def serialize_validator(klass, obj):
    """Validates a handler implementation against the ISerialize interface."""
    members = [
        'setup',
        'load',
        'dump',
        'get_headers',
        ]
    interface.validate(ISerialize, obj, members)
    
class ISerialize(interface.Interface):
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
    
    def setup():
        """
        The setup function is called during connection initialization and
        must 'setup' the handler object making it ready for the connection
        or the application to make further calls to it.
        
        This function takes no arguments.

        Returns: n/a
        
        """
    
    def get_headers():
        """
        Return a dictionary of additional headers to include in requests.
        
        """
        
    def load():
        """
        Load a serialized string and return a dictionary of key/value pairs.
        
        Required Arguments:
        
            serialized_data
                A string of serialzed data.
        
        Returns: dict
        
        """
        
    def dump():
        """
        Dump a dictionary of values from a serialized string.
        
        Required Arguments:
                                
            data_dict
                A data dictionary to serialize.

        Returns: string
        
        """
        
class JsonSerializationHandler(object):
    def __init__(self):
        pass
    
    def setup(self):
        import json
        global json
        
    def get_headers(self):
        headers = {
            'Content-Type' : 'application/json',
            }
        return headers
        
    def load(self, serialized_string):
        try:
            return json.loads(serialized_string.strip('\n'))
        except ValueError, e:
            return dict(error=e.args[0])
    
    def dump(self, dict_obj):
        try:
            return json.dumps(dict_obj)
        except ValueError, e:
            return json.dumps(dict(error=e.args[0]))
            
class YamlSerializationHandler(object):
    def __init__(self):
        pass
    
    def setup(self):
        import yaml
        global yaml
        
    def load(self, dict_obj):
        return yaml.loads(dict_obj)
    
    def dump(self, dict_obj):
        return yaml.dump(dict_obj)