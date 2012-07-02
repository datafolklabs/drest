
from drest import exc, meta, interface

def validate(obj):
    """Validates a handler implementation against the IResponse interface."""
    members = [
        'status',
        'data',
        ]
    metas = []
    interface.validate(IResponse, obj, members, metas)
    
class IResponse(interface.Interface):
    """
    This class defines the Response Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    All implementations must provide sane 'default' functionality when 
    instantiated with no arguments.  Meaning, it can and should accept 
    optional parameters that alter how it functions, but can not require
    any parameters.  
    
    Implementations do *not* subclass from interfaces.
            
    """
    status = interface.Attribute('The response status (i.e. HTTP code).')
    data = interface.Attribute('The data returned by the request.')
    headers = interface.Attribute('The headers returned by the request.')
    
class ResponseHandler(meta.MetaMixin):
    class Meta:
        pass
    
    status = None
    data = None
    headers = None
    
    def __init__(self, status, data, headers):
        self.status = int(status)
        self.data = data
        self.headers = headers
