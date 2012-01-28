
class dRestError(Exception):
    """Generic dRest Errors."""
    def __init__(self, msg):
        self.msg = msg
    
    def __repr__(self):
        return self.msg
    
    def __str__(self):
        return self.msg
    
class dRestInterfaceError(dRestError):
    """dRest Interface Errors."""
    pass

class dRestRequestError(dRestError):
    """dRest Request Errors."""
    def __init__(self, msg, response, content):
        super(dRestRequestError, self).__init__(msg)
        self.response = response
        self.content = content
        
class dRestResourceError(dRestError):
    """dRest Resource Errors."""
    pass
        
class dRestAPIError(dRestError):
    """dRest API Errors."""
    pass
        