
import os
import json
from httplib2 import Http
from urllib import urlencode
from urllib2 import urlopen

class dRESTRequestError(object):
    pass

class dRESTConnectError(object):
    pass
        
class dRESTConnection(object):
    def __init__(self, end_point):
        self.end_point = end_point
        
    def auth
    
class dRESTResource(object):
    def __init__(self, end_point):
        self.end_point = end_point
        
    def auth(**kw):
        """
        Authenticate with the end point.  Some request handlers
        send auth info along with the request call, and therefore this method
        may not do anything.
        """
        raise NotImplementedError
        
    def request(path, params):
        """
        Make a request to the end-point.
        
        Required Arguments:
        
            path
                The path (from 'baseurl' to the resource/method)
            
        Optional Arguments:
        
            params
                Params to encode and pass to the request.
        
        """
        raise NotImplementedError
               
 
        
class LandGrabResource(object):
    def __init__(self, request_handler):
        self.request = request_handler.request
    
    def _alter_params(self, params):
        """
        Give the ability to alter params before sending the request.
        
        Required Arguments:
        
            params
                The list of params that will be passed to the hub.
                
        """
        return params

    def get(self, resource_id=None, filters={}, limit=100):
        """
        Get all records for a resource, or a single resource record.
        
        Optional Arguments:
        
            resource_id
                The resource id
        
            filters
                A dictionary of filter parameters.  For example 
                'dict(foo=bar)' will only return resources whose 'foo' is 
                equal to 'bar'.
            
            limit
                Limit the number of results.  Default: 100 (no limit).
                
        """

        if resource_id:
            path = '/%s/%s' % \
                    (self.resource, int(resource_id))
        else:
            path = '/%s' % self.resource
            
        res = self.request('GET', path, params=filters)
        return res
    
    def get_all(self, params={}):
        """
        Get all available members of a resource.  
        
        Optional Arguments:
        
            params
                All parameters are treated like 'filter' arguments.  Meaning
                if you pass 'params=dict(resource_id=1)' then all results will
                be filtered down to only those that have the user_id of '1'.
                A special parameter can be passed of 'landgrab_search_query' which
                triggers a regex search of specific resource items such as
                label, description, about, etc.
                
        """
        try:    
            assert isinstance(params, dict), "params must be of type 'dict'."
        except AssertionError, e:
            raise exc.LandGrabInterfaceError, e.args[0]
        params['_method'] = 'GET'
        res = self.request('/%s/get_all.json' % self.resource, params)
        return res
    
    def create(self, params={}):
        """
        Create a new resource.
        
        Required Arguments:
        
            params
                A dictionary of parameters (different for every resource).

        """
        try:    
            assert isinstance(params, dict), "params must be of type 'dict'."
        except AssertionError, e:
            raise exc.LandGrabInterfaceError, e.args[0]
            
        params = self._alter_params(params)
        path = '/%s' % self.resource
        res = self.request('POST', path, params)
        return res
        
    def update(self, resource_id, params={}):
        """
        Update an existing resource.
        
        Required Arguments:
        
            resource_id
                The id of the resource to update.
                
            params
                A dictionary of parameters (different for every resource).
                
        """        
        try:    
            resource_id = int(resource_id)
            assert isinstance(params, dict), "params must be of type 'dict'."
        except AssertionError, e:
            raise exc.LandGrabInterfaceError, e.args[0]
        except ValueError, e:
            raise exc.LandGrabInterfaceError, "resource id (int) required."
    
        params = self._alter_params(params)
        params['id'] = resource_id
        path = '/%s/%s' % (self.resource, resource_id)
        res = self.request('PUT', path, params)
        return res
        
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
        try:    
            resource_id = int(resource_id)
            assert isinstance(params, dict), "params must be of type 'dict'."
        except AssertionError, e:
            raise exc.LandGrabInterfaceError, e.args[0]
        except ValueError, e:
            raise exc.LandGrabInterfaceError, "resource id (int) required."

        path = '/%s/%s' % (self.resource, resource_id)
        res = self.request('DELETE', path, params)
        return res
        
class LandGrabRootResource(object):
    resource = 'root'
    def __init__(self, request_handler):
        self.request = request_handler.request

class LandGrabStatusResource(LandGrabResource):
    resource = 'status'
    pass

class LandGrabPlotResource(LandGrabResource):
    resource = 'plot'

    def find(self, query, limit=10):
        """
        Find a plot based on a search query.
        
        Required Arguments:
        
            query
                The search string.
                
        Optional Arguments:
        
            limit
                Limit the results.  Default: 10.
        
        """
        params = dict(query=query, limit=limit)
        res = self.request('/plot/find.json', params)
        return res

class LandGrabUserResource(LandGrabResource):
    resource = 'user'
    def __init__(self, request_handler):
        LandGrabResource.__init__(self, request_handler)
    
    def _alter_params(self, params):
        if params.has_key('agreed_to_terms'):
            if params['agreed_to_terms'] in [True, 'True', 'true', '1', 1]:
                params['agreed_to_terms'] = 1
        return params
    
    def get_session_identity(self):
        res = self.request('/user/get_session_identity', dict())
        return res
        
class LandGrabInterface(object):
    """
    The LandGrabInterface class can be used to interface with a LandGrab hub.  
    
    Required Arguments:
    
        request_handler
            An instantiated LandGrabRequestHandler interface object.
    
    Usage:
    
    .. code-block:: python
    
        from landgrab.interface import v0
        
        handler = v0.LandGrabAPIKeyRequestHandler('https://api-v0.landgrab.com')
        handler.auth(user='john', api_key='XXXXX')
        hub = v0.LandGrabInterface(request_handler=handler)
        
        res = hub.user.get_one(342)
        
        res = hub.user.get_all()
        
        ...
        
            
    
    See the documentation for each resource for full examples of their use.
        
    """
    def __init__(self, request_handler=None):
        #try:
        #    assert LandGrabRequestHandler.providedBy(request_handler), \
        #        "Request handler object does not provide LandGrabRequestHandler!"
        #except AssertionError, e:
        #    raise exc.LandGrabInterfaceError, e.args[0]
            
        self.root = LandGrabRootResource(request_handler)     
        self.status = LandGrabStatusResource(request_handler)
        self.plot = LandGrabPlotResource(request_handler)
        self.user = LandGrabUserResource(request_handler)
        self.request = request_handler.request