dRest HTTP/REST Client Library for Python
=========================================

dRest is a configurable HTTP/REST client library for Python.  It's goal is to
make the creation of API clients dead simple, without lacking features.

[![Continuous Integration Status](https://secure.travis-ci.org/datafolklabs/drest.png)](http://travis-ci.org/datafolklabs/drest/)

Features include:

 * Light-weight API Client Library, implementing REST by default
 * Native support for the Django TastyPie API Framework
 * Only one external dependency on httplib2
 * Key pieces of the library are customizable by defined handlers
 * Interface definitions ensure handlers are properly implemented
 * Tested against Python versions 2.6, 2.7, 3.2, 3.3
 * 100% test coverage via Nose

More Information
----------------

 * RTFD: http://drest.rtfd.org/
 * CODE: http://github.com/datafolklabs/drest/
 * PYPI: http://pypi.python.org/pypi/drest/
 * T-CI: http://travis-ci.org/datafolklabs/drest/

Usage
-----

```python
import drest

# Create a generic client api object
api = drest.API('http://localhost:8000/api/v1/')

# Make calls openly via any HTTP Method, and any path
# GET http://localhost:8000/api/v1/users/1/
response = api.make_request('GET', '/users/1/')

# Or attach a resource
api.add_resource('users')

# Get available resources
api.resources
>>> ['users', 'projects', 'etc']

# Get all objects of a resource
# GET http://localhost:8000/api/v1/users/
response = api.users.get()

# Get a single resource with primary key '1'
# GET http://localhost:8000/api/v1/users/1/
response = api.users.get(1)

# Create a resource data dictionary
user_data = dict(
    username='john.doe',
    password='oober-secure-password',
    first_name='John',
    last_name='Doe',
    )

# POST http://localhost:8000/api/v1/users/
response = api.users.post(user_data)

# Update a resource with primary key '1'
response = api.users.get(1)
updated_data = response.data.copy()
updated_data['first_name'] = 'John'
updated_data['last_name'] = 'Doe'

# PUT http://localhost:8000/api/v1/users/1/
response = api.users.put(1, updated_data)

# Patch a resource with primary key '1'
# PATCH http://localhost:8000/api/v1/users/1/
response = api.users.patch(1, dict(first_name='Johnny'))

# Delete a resource with primary key '1'
# DELETE http://localhost:8000/api/v1/users/1/
response = api.users.delete(1)

# Get the status of the request
response.status

# Or the data returned by the request
response.data

# Or the headers returned by the request
response.headers
```

License
-------

The dRest library is Open Source and is distributed under the BSD License
(three clause).  Please see the LICENSE file included with this software.
