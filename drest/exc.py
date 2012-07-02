
class dRestError(Exception):
    """Generic dRest Errors."""
    def __init__(self, msg):
        self.msg = msg
    
    def __repr__(self):
        return "<dRestError: %s>" % self.msg
    
    def __str__(self):
        return self.msg
    
class dRestInterfaceError(dRestError):
    """dRest Interface Errors."""
    
    def __init__(self, msg):
        super(dRestInterfaceError, self).__init__(msg)
    
    def __repr__(self):
        return "dRestInterfaceError: %s" % self.msg
        
class dRestRequestError(dRestError):
    """dRest Request Errors."""
    def __init__(self, msg, response):
        super(dRestRequestError, self).__init__(msg)
        self.response = response
    
    def __repr__(self):
        return "dRestRequestError: %s" % self.msg
            
class dRestResourceError(dRestError):
    """dRest Resource Errors."""
    
    def __init__(self, msg):
        super(dRestResourceError, self).__init__(msg)
    
    def __repr__(self):
        return "dRestResourceError: %s" % self.msg
        
class dRestAPIError(dRestError):
    """dRest API Errors."""
    
    def __init__(self, msg):
        super(dRestAPIError, self).__init__(msg)
    
    def __repr__(self):
        return "dRestAPIError: %s" % self.msg
        