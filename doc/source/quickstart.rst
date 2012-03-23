Quickstart Guide
================
    
A REST Client Example
---------------------

Note that the following is all fictitious data.  What is received from and
sent to an API is unique to every API.  Do not copy and paste these examples.

Connecting with an API
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    import drest
    api = drest.API('http://localhost:8000/api/v1/')
    
Authentication
^^^^^^^^^^^^^^

By default, drest.api.API.auth() implements HTTP Basic Authentication.  This 
is generally overridden however by specific API's that subclass from api.API().
    
.. code-block:: python

    api.auth('john.doe', 'my_password')
    
    
Note that authentication may not be necessary for your use case, or for 
read-only API's.

Making Requests
^^^^^^^^^^^^^^^

Requests can be made openly by specifying the method 
(GET, PUT, POST, DELETE, ...), as well as the path (after the baseurl).

.. code-block:: python

    # GET http://localhost:8000/api/v1/users/1/
    response = api.make_request('GET', '/users/1/')

Additionally, you can add a resource which makes access to the API more 
native and programatic.

.. code-block:: python

    # Add a basic resource (assumes path='/users/')
    api.add_resource('users')
    
    # A list of available resources is available at:
    api.resources
    
    # GET http://localhost:8000/api/v1/users/
    response = api.users.get()
    
    # GET http://localhost:8000/api/v1/users/1/
    response = api.users.get(1)


Creating a resource only requires a dictionary of 'parameters' passed to the
resource:

.. code-block:: python

    user_data = dict(
        username='john.doe', 
        password='oober-secure-password',
        first_name='John',
        last_name='Doe',
        )
    
    # POST http://localhost:8000/api/v1/users/
    response = api.users.post(user_data)

Updating a resource is as easy as requesting data for it, modifying it, and
sending it back

.. code-block:: python

    response = api.users.get(1)
    updated_data = response.data.copy()
    updated_data['first_name'] = 'John'
    updated_data['last_name'] = 'Doe'
    
    # PUT http://localhost:8000/api/v1/users/1/
    response = api.users.put(1, updated_data)
    
    
Deleting a resource simply requires the primary key:

.. code-block:: python

    # DELETE http://localhost:8000/api/v1/users/1/
    response = api.users.delete(1)    

    
Working With Return Data
------------------------

Every call to an API by default returns a drest.response.ResponseHandler
object.  The two most useful members of this object are:

    * response.status (http status code)
    * response.data (the data returned by the api)


If a serialization handler is used, then response.data will be the 
unserialized form (Python dict).

The Response Object
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    response = api.users.get()
    response.status # 200
    response.data # dict
    
    
Developers can base conditions on the status of the response (or other
fields):

.. code-block:: python

    response = api.users.get()
    if response.status != 200:
        print 'Uhoh.... we didn't get a good response.'


The data returned from a request is the data returned by the API.  This is 
generally JSON, YAML, XML, etc... however if a Serialization handler is 
enabled, this will be a python dictionary.  See :mod:`drest.serialization`.

response.data:
    
.. code-block:: python
    
    {
        u'meta': 
            {
                u'previous': None, 
                u'total_count': 3, 
                u'offset': 0, 
                u'limit': 20, 
                u'next': 
                None
            }, 
        u'objects': 
            [
                {
                    u'username': u'john.doe', 
                    u'first_name': u'John', 
                    u'last_name': u'Doe', 
                    u'resource_pk': 2, 
                    u'last_login': u'2012-01-26T01:21:20', 
                    u'resource_uri': u'/api/v1/users/2/', 
                    u'id': u'2', 
                    u'date_joined': u'2008-09-04T14:25:29'
                }
            ]
    }

The above is fictitious data returned from a TastyPie API.  What is returned
by an API is unique to that API therefore you should expect the 'data' to be
different that the above.


Connecting Over SSL
-------------------

Though this is documented elsewhere, it is a pretty common question.  Often
times API services are SSL enabled (over https://) but do not possess a valid
or active SSL certificate.  Anytime an API service has an invalid, or usually
self-signed certificate, you will receive an SSL error similar to:

.. code-block:: text

    [Errno 1] _ssl.c:503: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed
    

In order to work around such situations, simply pass the following to your 
api:

.. code-block:: python

    api = drest.API('https://example.com/api/v1/', ignore_ssl_validation=True)
    

    