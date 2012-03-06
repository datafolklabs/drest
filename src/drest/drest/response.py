
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

class ResponseHandler(meta.MetaMixin):
    class Meta:
        pass
    
    status = None
    data = None
    
    def __init__(self, status, data, **kw):
        self.status = int(status)
        self.data = data
