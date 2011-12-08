
class dRESTError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __repr__(self):
        return self.msg
    
    def __str__(self):
        return self.msg
    
class dRESTInterfaceError(dRESTError):
    pass

class dRESTRequestError(dRESTError):
    pass

class dRESTConnectError(dRESTError):
    pass
        