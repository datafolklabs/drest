
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
        self.msg = msg
        self.response = response
        self.content = content
        super(dRestRequestError, self).__init__(msg)
        
class dRestConnectionError(dRestError):
    pass
        