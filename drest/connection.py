
from drest import interface, resource, request, serialization

class Connection(object):
    def __init__(self, baseurl, **kw):
        self.baseurl = baseurl
        self.request_handler = kw.get('request_handler', None)
        self.default_resource_handler = kw.get('default_resource_handler',
                                               resource.RESTResourceHandler)
        self.serialization_handler = kw.get('serialization_handler', None)
        self.serialize = kw.get('serialize', True)
        self.deserialize = kw.get('deserialize', True)
        self._setup()
        
    def _setup(self):
        self._setup_serialization_handler()
        self._setup_request_handler()
        
    def _setup_request_handler(self):
        if not self.request_handler:
            self.request_handler = request.HTTPRequestHandler()
        self.request_handler.setup(self.baseurl, 
                                   serialization_handler=self.serialization_handler,
                                   serialize=self.serialize,
                                   deserialize=self.deserialize)
        
    def _setup_serialization_handler(self):
        if not self.serialize and not self.deserialize:
            self.serialization_handler = None
            return
            
        if not self.serialization_handler:
            self.serialization_handler = serialization.JsonSerializationHandler()
        serialization.serialize_validator(serialization.ISerialize, 
                                          self.serialization_handler)
        self.serialization_handler.setup()
        
    def auth(self, *args, **kw):
        self.request_handler.auth(*args, **kw)
        
    def request(self, method, path, params={}):
        return self.request_handler.request(method, path, params)
        
    def add_resource(self, name, resource_handler=None, path=None):
        if not path:
            path = '%s' % name
        else:
            path = path.lstrip('/')
            
        if not resource_handler:
            handler = self.default_resource_handler()
        else:
            handler = resource_handler
        resource.resource_validator(resource.IResource, handler)
        handler.setup(name, path, self.request_handler)
        
        setattr(self, name, handler)
        
