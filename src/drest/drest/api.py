"""dRest core API connection library."""

from drest import interface, resource, request, serialization, meta, exc

class API(meta.MetaMixin):
    class Meta:
        baseurl = None
        request = request.RequestHandler
        resource = resource.RESTResourceHandler

    resources = []
    
    def __init__(self, baseurl=None, **kw):
        kw['baseurl'] = kw.get('baseurl', baseurl)
        super(API, self).__init__(**kw)        
        self._request = self._meta.request(baseurl=self._meta.baseurl)

    def auth(self, *args, **kw):
        self._request.auth(*args, **kw)
        
    def request(self, method, path, params={}):
        return self._request.request(method, path, params)
        
    def add_resource(self, name, resource_handler=None, path=None):
        if not path:
            path = '%s' % name
        else:
            path = path.lstrip('/')
            
        if not resource_handler:
            handler = self._meta.resource
        else:
            handler = resource_handler
        
        handler = handler(baseurl=self._meta.baseurl, path=path, resource=name)
        
        resource.resource_validator(resource.IResource, handler)
        if hasattr(self, name):
            raise exc.dRestResourceError(
                "The object '%s' already exist on '%s'" % (name, self))
        setattr(self, name, handler)
        self.resources.append(name)
        
class TastyPieAPI(API):
    class Meta:
        request = request.TastyPieRequestHandler
        resource = resource.TastyPieResourceHandler
        auto_detect_resources = True
        
    def __init__(self, baseurl=None, **kw):
        super(TastyPieAPI, self).__init__(baseurl, **kw)
        if self._meta.auto_detect_resources:
            self.find_resources()

    def find_resources(self):
        response, data = self.request('GET', '/')
        for resource in data.keys():
            self.add_resource(resource)
    