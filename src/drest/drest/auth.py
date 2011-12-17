"""dREST Authentication Module."""

from drest.core import exc, interface

def auth_validator(klass, obj):
    """Validates a handler implementation against the IAuth interface."""
    members = [
        'setup',
        'get_auth_params', 
        ]
    interface.validate(IAuth, obj, members, meta)
    
class IAuth(interface.Interface):
    """
    This class defines the Authentication Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    All implementations must provide sane 'default' functionality when 
    instantiated with no arguments.  Meaning, it can and should accept 
    optional parameters that alter how it functions, but can not require
    any parameters.  
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from drest.core import auth
        
        class MyAuthHandler(object):
            class meta:
                interface = auth.IAuth
            ...
            
    """
    validate = auth_validator
    
    def setup(request_handler):
        """
        The setup function is called during connection initialization and
        must 'setup' the handler object making it ready for the connection
        or the application to make further calls to it.
        
        Required Arguments:
        
            end_point
                The base url endpoint
            request_handler
                A request
                
        Returns: n/a
        
        """
    
    def get_auth_params():
        """
        Authenticate against the connection.  This might mean making OAuth
        calls to obtain a request token, or simply setting user and API Key
        parameters.
        
        Must return a dictionary of parameters to add to each request (i.e
        dict(user='some_user', api_key='XXXXXXXXX'))
        
        Returns: dict()
        
        """

class UserKeyAuthHandler(object):
    user_param = 'user'
    api_key_param = 'api_key'
        
    def get_auth_params(self, user, api_key):
        res = dict()
        res[self.user_param] = user
        res[self.api_key_param] = api_key
        return res