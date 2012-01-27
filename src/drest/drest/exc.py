
class dRestError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __repr__(self):
        return self.msg
    
    def __str__(self):
        return self.msg
    
class dRestInterfaceError(dRestError):
    pass

class dRestRequestError(dRestError):
    def __init__(self, msg, response, content):
        super(dRestRequestError, self).__init__(msg)
        self.response = response
        self.content = content
        
class dRestResourceError(dRestError):
    pass
        
class dRestAPIError(dRestError):
    pass
        