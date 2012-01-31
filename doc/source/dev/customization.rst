Customizing dRest
=================

Every piece of dRest is completely customizable by way of 'handlers'.  

API Reference:

    * :mod:`drest.resource`
    * :mod:`drest.request`
    * :mod:`drest.serialization`

Example
-------

.. code-block:: python

    import drest
    
    class MySerializationHandler(drest.serialization.SerializationHandler):        
        def serialize(self, data_dict):
            # do something to serialize data dictionary
            ...
    
        def deserialize(self, serialized_data):
            # do something to deserialize data
            ...
    
    class MyRequestHandler(drest.request.RequestHandler):
        class Meta:
            serialization = MySerializationHandler
        
    
    class MyResourceHandler(drest.resource.ResourceHandler):
        class Meta:
            request = MyRequestHandler
    
        def some_custom_function(self, params={}):
            # do some kind of custom api call
            ...

    class MyAPI(drest.api.API):
        class Meta:
            baseurl = 'http://example.com/api/v1/'
            resource = MyResourceHandler
            request = MyRequestHandler
    
    api = MyAPI()
    api.add_resource('users')
    api.users.get()
    api.users.get(<id>)
    api.users.put(<id>, data_dict)
    api.users.post(data_dict)
    api.users.delete(<id>)
    api.users.some_custom_function()