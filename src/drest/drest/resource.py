
import re
from drest import interface, exc, meta, request

def validate(obj):
    """Validates a handler implementation against the IResource interface."""
    members = []
    metas = [
        'baseurl',
        'resource',
        'path',
        'request',
        ]
    interface.validate(IResource, obj, members)
    
class IResource(interface.Interface):
    """
    This class defines the Resource Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    All implementations must provide sane 'default' functionality when 
    instantiated with no arguments.  Meaning, it can and should accept 
    optional parameters that alter how it functions, but can not require
    any parameters.  
    
    Implementations do *not* subclass from interfaces.
            
    """
    
        
class ResourceHandler(meta.MetaMixin):
    """
    This class acts as a base class that other resource handler should
    subclass from.
    
    """
    class Meta:
        pass
        
    def __init__(self, api_obj, name, path, **kw):
        super(ResourceHandler, self).__init__(**kw)        
        self.api = api_obj
        self.path = path
        self.name = name
        
class RESTResourceHandler(ResourceHandler):
    """
    This class implements the IResource interface, specifically for 
    interacting with REST-like resources.  It provides convenient functions
    that wrap around the typical GET, PUT, POST, DELETE actions.
    
    Optional Arguments / Meta:
    
        api_obj
            The api (parent) object that this resource is being attached to.
        
        name
            The name of the resource on the API.
            
        path
            The path to the resource (after api.baseurl).
            
    Usage:
    
    .. code-block:: python
    
        import drest
        
        class MyAPI(drest.api.API):
            class Meta:
                resource_handler = drest.resource.RESTResourceHandler
        ...
        
    """
    def __init__(self, api_obj, name, path, **kw):
        super(RESTResourceHandler, self).__init__(api_obj, name, path, **kw)
                
    def filter(self, params):
        """
        Give the ability to alter params before sending the request.
        
        Required Arguments:
        
            params
                The list of params that will be passed to the endpoint.
                
        """
        return params

    def get(self, resource_id=None, params={}):
        """
        Get all records for a resource, or a single resource record.
        
        Optional Arguments:
        
            resource_id
                The resource id (may also be a label in some environments).
        
            params
                Additional request parameters to pass along.
                
        """

        if resource_id:
            path = '/%s/%s' % (self.path, resource_id)
        else:
            path = '/%s' % self.path
            
        try:
            response, content = self.api.make_request('GET', path, 
                                             params=self.filter(params))
        except exc.dRestRequestError as e:
            msg = "%s (resource: %s, id: %s)" % (e.msg, self.name, 
                                                 resource_id)
            raise exc.dRestRequestError(msg, e.response, e.content)
                                        
        return response, content
    
    def create(self, params={}):
        """A synonym for self.post()."""
        return self.post(params)
        
    def post(self, params={}):
        """
        Create a new resource.
        
        Required Arguments:
        
            params
                A dictionary of parameters (different for every resource).

        """
        params = self.filter(params)
        path = '/%s' % self.path
        
        try:
            response, content = self.api.make_request('POST', path, self.filter(params))
        except exc.dRestRequestError as e:
            msg = "%s (resource: %s)" % (e.msg, self.name)
            raise exc.dRestRequestError(msg, e.response, e.content)
            
        return response, content
        
    def update(self, resource_id, params={}):
        """A synonym for self.put()."""
        return self.put(resource_id, params)
        
    def put(self, resource_id, params={}):
        """
        Update an existing resource.
        
        Required Arguments:
        
            resource_id
                The id of the resource to update.
                
            params
                A dictionary of parameters (different for every resource).
                
        """
                    
        params = self.filter(params)
        path = '/%s/%s' % (self.path, resource_id)
        
        try:
            response, content = self.api.make_request('PUT', path, params)
        except exc.dRestRequestError as e:
            msg = "%s (resource: %s, id: %s)" % (e.msg, self.name, 
                                                 resource_id)
            raise exc.dRestRequestError(msg, e.response, e.content)
            
        return response, content
        
    def delete(self, resource_id, params={}):
        """
        Delete resource record.
        
        Required Arguments:
        
            resource_id
                The resource id
        
        Optional Arguments:
        
            params
                Some resource might allow additional parameters.  For example,
                the user resource has a 'rdikwid' (really delete I know what 
                I'm doing) option which causes a user to *really* be deleted 
                (normally deletion only sets the status to 'Deleted').
            
        """
        path = '/%s/%s' % (self.path, resource_id)
        try:
            response, content = self.api.make_request('DELETE', path, params)
        except exc.dRestRequestError as e:
            msg = "%s (resource: %s, id: %s)" % (e.msg, self.name, 
                                                 resource_id)
            raise exc.dRestRequestError(msg, e.response, e.content)
            
        return response, content

class TastyPieResourceHandler(RESTResourceHandler):
    """
    This class implements the IResource interface, specifically tailored for
    interfacing with `TastyPie <http://django-tastypie.readthedocs.org/en/latest>`_.
    
    """ 
    class Meta:
        request = request.TastyPieRequestHandler
        schema = None
        full_url = None
        
    def __init__(self, api_obj, name, path, **kw):
        super(TastyPieResourceHandler, self).__init__(api_obj, name, path, **kw)
        
    def get_by_uri(self, resource_uri, params={}):
        """
        A wrapper around self.get() that accepts a TastyPie 'resource_uri' 
        rather than a 'pk' (primary key).
        
        Required Arguments:
        
            resource_uri
                The Resource URI to GET.
            
        Optional Arguments
            
            params
                All additional keyword arguments are passed as extra request
                parameters.
        
        Usage
        
        .. code-block:: python
        
            import drest
            api = drest.api.TastyPieAPI('http://localhost:8000/api/v0/')
            api.auth(user='john.doe', api_key='34547a497326dde80bcaf8bcee43e3d1b5f24cc9')
            response, data = api.users.get_by_uri('/api/v1/users/234/')
            
        """
        resource_uri = resource_uri.rstrip('/')
        pk = resource_uri.split('/')[-1]
        return self.get(pk, params)

    @property
    def schema(self):
        """
        Returns the resources schema.
        
        """
        if not self._meta.schema:
            response, data = self.api.make_request('GET', '%s/schema' % self.path)
            self._meta.schema = data
            
        return self._meta.schema