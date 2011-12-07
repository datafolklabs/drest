
from drest import resource, request

class Connection(object):
    def __init__(self, baseurl, **kw):
        self.baseurl = baseurl
        self.request_handler = kw.get('request_handler', None)
        self.default_resource_handler = kw.get('default_resource_handler',
                                               resource.RESTResource)
        #self.serialization_handler = kw.get('serialization_handler', None)                 
        self._setup()
        
    def _setup(self):
        self._setup_request_handler()
        #self._setup_auth_handler()
        
    def _setup_request_handler(self):
        if not self.request_handler:
            self.request_handler = request.HTTPRequestHandler()
        self.request_handler.setup(self.baseurl)
        
    def auth(self, *args, **kw):
        self.request_handler.auth(*args, **kw)
        
    def request(self, method, path, params={}):
        return self.request_handler.request(method, path, params)
        
    def add_resource(self, name, resource_handler, path=None):
        handler = self.orig_request_handler('%s/%s' % (self.baseurl, path))
        setattr(self, name, handler)
        
