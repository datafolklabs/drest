Quick Start Guide
=================

The following outlines installation of dRest, as well as quick starting a
new api client.

Installation
------------

It is recommended to work out of a `VirtualENV <http://pypi.python.org/pypi/virtualenv>`_ 
for development, which is reference throughout this documentation.  VirtualENV
is easily installed on most platforms either with 'easy_install' or 'pip' or
via your OS distributions packaging system (yum, apt, brew, etc).

Creating a Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    $ virtualenv --no-site-packages ~/env/drest/
    
    $ source ~/env/drest/bin/activate
    

When installing drest, ensure that your development environment is active
by sourcing the activate script (as seen above).


Installing Development Version From Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    (drest) $ git clone git://github.com/derks/drest.git
    
    (drest) $ cd src/drest/
    
    (drest) $ python setup.py install
    

To run tests, do the following from the 'root' directory:

.. code-block:: text
    
    (drest) $ pip install nose
    
    (drest) $ python setup.py nosetests


Installing Stable Versions From PyPi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    $ pip install drest
    
    
A REST Client Example
---------------------

Note that the following is all fictitious data.  What is received from and
sent to an API is unique to every API.  Do not copy and paste these examples.

.. code-block:: python
    
    import drest

    # Create a generic client api object
    api = drest.API('http://localhost:8000/api/v1/')
    
    # By default, auth() just appends its params to the URL so name the
    # parameters however you want them passed as.
    api.auth(api_user='john.doe', password='XXXXXXXXXXXX')
    
    # Make calls openly
    response, data = api.request('GET', '/users/1/')
    
    # Or attach a resource
    api.add_resource('users')
    
    # Get available resources
    api.resources
    
    # Get all objects of a resource
    response, objects = api.users.get()
    
    # Get a single resource with primary key '1'
    response, object = api.users.get(1)
    
    # Update a resource with primary key '1'
    response, data = api.users.get(1)
    updated_data = data.copy()
    updated_data['first_name'] = 'John'
    updated_data['last_name'] = 'Doe'
    
    response, object = api.users.update(data['id'], updated_data)
    
    # Create a resource
    user_data = dict(
                    username='john.doe',
                    password'oober-secure-password',
                    first_name='John',
                    last_name'Doe',
                    )
    response, data = api.users.create(user_data)
    
    # Delete a resource with primary key '1'
    response, data = api.users.delete(1)    

    