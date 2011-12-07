
class RESTResource(object):
    def __init__(self):
        self.resource = None
        self.path = None
        self.request_handler = None
        
    def setup(self, resource, path, request_handler):
        self.request = request_handler.request
        
    def request(self, method, params):
        self.request_handler.request(method, self.path, params)
        
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
                Additional GET parameters to pass along.
                
        """

        if resource_id:
            path = '/%s/%s' % (self.resource, resource_id)
        else:
            path = '/%s' % self.resource
            
        res = self.request('GET', path, params=self.filter(params))
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
        res = self.request('POST', path, self.filter(params))
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