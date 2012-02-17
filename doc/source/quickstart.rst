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
    response, data = api.request('GET', '/users/1/')

Additionally, you can add a resource which makes access to the API more 
native and programatic.

.. code-block:: python

    api.add_resource('users')
    
    # A list of available resources is available at:
    api.resources
    
    # GET http://localhost:8000/api/v1/users/
    response, data = api.users.get()
    
    # GET http://localhost:8000/api/v1/users/1/
    response, data = api.users.get(1)


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
    response, data = api.users.post(user_data)

Updating a resource is as easy as requesting data for it, modifying it, and
sending it back

.. code-block:: python

    response, data = api.users.get(1)
    updated_data = data.copy()
    updated_data['first_name'] = 'John'
    updated_data['last_name'] = 'Doe'
    
    # PUT http://localhost:8000/api/v1/users/1/
    response, data = api.users.put(data['id'], updated_data)
    
    
Deleting a resource simply requires the primary key:

.. code-block:: python

    # DELETE http://localhost:8000/api/v1/users/1/
    response, data = api.users.delete(1)    

    
Working With Return Data
------------------------

Every call to an API returns a tuple in the form of:

.. code-block:: python

    (response, return_data)

The Response Object
^^^^^^^^^^^^^^^^^^^

The first item returned from a request is an `httplib2.Response <http://bitworking.org/projects/httplib2/doc/html/libhttplib2.html#httplib2.Response>`_ 
object that contains response data. It can can also be accessed as a 
dictionary:

.. code-block:: python

    response, data = api.users.get()
    
    # The contents of the response object:
    {
        'status': '200', 
        'content-location': u'http://localhost:8000/api/v1/users/', 
        'vary': 'Cookie', 
        'server': 'WSGIServer/0.1 Python/2.7.2', 
        'date': 'Tue, 31 Jan 2012 20:41:47 GMT', 
        'content-type': 'application/json; charset=utf-8',
    }
    
Developers can base conditions on the status of the response (or other
fields):

.. code-block:: python

    response, data = api.users.get()
    if int(response.status) != 200:
        print 'Uhoh.... we didn't get a good response.'


The Return Data
^^^^^^^^^^^^^^^

The second item returned from a request is the data, or content, returned by
the API.  This is generally JSON, YAML, XML, etc... however if a Serialization
handler is enabled, this will be a python dictionary.  
See :mod:`drest.serialization`.

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
    

    