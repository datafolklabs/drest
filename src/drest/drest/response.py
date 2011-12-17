
from drest import exc, interface

def validate(obj):
    """Validates a handler implementation against the ISerialize interface."""
    members = [
        'setup',
        'handle_response',
        ]
    interface.validate(IResponse, obj, members)
    
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
    
    def setup():
        """
        The setup function is called during connection initialization and
        must 'setup' the handler object making it ready for the connection
        or the application to make further calls to it.
        
        This function does not take any parameters.
                
        Returns: n/a
        
        """
    
    def handle_response(response, content):
        """
        Perform any actions necessary to handle the reponse.
        
        Required Arguments:
        
            response
                The HTTP response data.
                
            content
                The content of the reponse.
            
        Returns: (response, content)
        
        """
    
class ResponseHandler(object):
    """
    This is a generic response handler which implements the IResponse
    interface.  It literally does nothing to handler a response.
    
    """
    def __init__(self):
        pass
        
    def setup(self):
        """
        Do nothing.
        
        """
        pass
    
    def handle_response(self, response, content):
        """
        Do nothing, and return the original response and content data.
        
        """
        return (response, content)
