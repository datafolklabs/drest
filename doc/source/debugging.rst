Debugging Requests
==================

Often times in development, making calls to an API can be obscure and 
difficult to work with especially when receiving 500 Internal Server Errors
with no idea what happens.  In browser development, most frameworks like 
Django or the like provide some sort of debugging interface allowing 
developers to analyze tracebacks, and what not.  Not so much when developing
command line apps or similar.

Enabling Debug Output
---------------------

In order to enable DEBUG output for every request, simply set the 'DREST_DEBUG'
environment variable to 1:

.. code-block:: text

    $ set DREST_DEBUG=1
    
    $ python test.py
    DREST_DEBUG: method=POST url=http://localhost:8000/api/v0/systems/ params={} headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey john.doe:XXXXXXXXXXXX'}
    
In the above, test.py just made a simple api.system.post() call which 
triggered DREST_DEBUG output.  In the output you have access to a number of 
things:

    method
        This is the method used to make the request.
        
    url
        The full url path of the request
    
    params
        Any parameters passed with the request
    
    headers
        Any headers passed with the request
    
Once done debugging, just disable DREST_DEBUG:

.. code-block:: text

    $ unset DREST_DEBUG
        
Viewing Upstream Tracebacks
---------------------------

If the error is happening server side, like a 500 Internal Server Error, you
will likely receive a traceback in the return content (at least during 
development).  This of course depends on the API you are developing against,
however the following is common practice in development:

.. code-block:: python

    try:
        response, data = api.my_resource.get()
    except drest.exc.dRestRequestError as e:
        print e.response
        print e.content

The above gives you the response object, as well as the content (data)... this
is useful because the exception is triggered in drest code and not your own 
(therefore bringing response, content back down the stack where you can 
use it).

