Customizing dRest
=================

Every piece of dRest is completely customizable by way of 'handlers'.  

API Reference:

    * :mod:`drest.api`
    * :mod:`drest.resource`
    * :mod:`drest.request`
    * :mod:`drest.response`
    * :mod:`drest.serialization`

Example
-------

The following is just a quick glance at what it would look to chain together
a custom Serialization Handler, Request Handler, Resource Handler, and 
finally a custom API client object.  This is not meant to be comprehensive 
by any means. In the real world, you will need to read the source code
documentation listed above and determine a) what you need to customize, and
b) what functionality you need to maintain.

.. code-block:: python

    import drest
    
    class MySerializationHandler(drest.serialization.SerializationHandler):        
        def serialize(self, data_dict):
            # do something to serialize data dictionary
            pass
    
        def deserialize(self, serialized_data):
            # do something to deserialize data
            pass
    
    class MyResponseHandler(drest.response.ResponseHandler)
        def __init__(self, status, data, **kw):
            super(MyResponseHandler, self).__init__(status, data, **kw)
            # do something to customize the response handler        
            
    class MyRequestHandler(drest.request.RequestHandler):
        class Meta:
            serialization_handler = MySerializationHandler
            response_handler = MyResponseHandler
            
        def handle_response(self, response):
            # do something to wrape every response
            pass
    
    class MyResourceHandler(drest.resource.ResourceHandler):
        class Meta:
            request_handler = MyRequestHandler
    
        def some_custom_function(self, params=None):
            if params is None:
                params = {}
            # do some kind of custom api call
            return self.request('GET', '/users/some_custom_function', params)

    class MyAPI(drest.api.API):
        class Meta:
            baseurl = 'http://example.com/api/v1/'
            resource_handler = MyResourceHandler
            request_handler = MyRequestHandler
        
        def auth(self, *args, **kw):
            # do something to customize authentication
            pass
    
    api = MyAPI()
    
    # Add resources
    api.add_resource('users')
    api.add_resource('projects')
    
    # GET http://example.com/api/v1/users/
    api.users.get()
    
    # GET http://example.com/api/v1/users/133/
    api.users.get(133)
    
    # PUT http://example.com/api/v1/users/133/
    api.users.put(133, data_dict)
    
    # POST http://example.com/api/v1/users/
    api.users.post(data_dict)
    
    # DELETE http://example.com/api/v1/users/133/
    api.users.delete(133)
    
    # GET http://example.com/api/v1/users/some_custom_function/
    api.users.some_custom_function()
    
Note that the id '133' above is the fictitious id of a user resource.
