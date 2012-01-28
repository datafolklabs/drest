
import os
import httplib
import socket
from httplib2 import Http
from urllib import urlencode
from urllib2 import urlopen

from drest import exc, interface, meta, serialization

def validate(klass, obj):
    """Validates a handler implementation against the IRequest interface."""
    members = [
        'add_param',
        'add_url_param',
        'add_header',
        'request',
        'extra_params',
        'extra_url_params',
        'extra_headers',
        'handle_response',
        ]
    interface.validate(IRequest, obj, members)
    
class IRequest(interface.Interface):
    """
    This class defines the Request Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    All implementations must provide sane 'default' functionality when 
    instantiated with no arguments.  Meaning, it can and should accept 
    optional parameters that alter how it functions, but can not require
    any parameters.  
    
    Implementations do *not* subclass from interfaces.
            
    """
    
    extra_params = interface.Attribute('Parameters to attach to the request data.')
    extra_url_params = interface.Attribute('Parameters to attach to the url.')
    extra_headers = interface.Attribute('Headers to pass with each request.')
    
    def add_param(key, value):
        """
        Add extra parameters to pass along with the url for *every* request.
        
        Required Arguments:
        
            key
                The key of the parameter to add.
            
            value
                The value of the parameter to add.
                
        """
        
    def add_header(key, value):
        """
        Add extra headers to pass along with *every* request.
        
        Required Arguments:
        
            key
                The key of the header to add.
            
            value
                The value of the header to add.
                
        """
    
    def auth():
        """
        Perform authentication with the upstream API.  This does not have 
        any required arguments, but is expected that the implementation will
        define those.
        
        """
        
    def request(method, path, params={}, headers={}):
        """
        Make a request with the upstream API.
        
        Required Arguments:
        
            method
                The HTTP method to request as.  I.e. ['GET', 'POST', 'PUT', 'DELETE'].
        
            path
                The of the request url *after* the baseurl.
            
            
        Optional Arguments:
        
            params
                Parameters to pass with the request.  These will be serialized
                if configured to serialize.
            
            headers
                Headers to pass to the request.
                
        """
    
    def handle_response(response, content):
        """
        Called after the request is made.  This is a convenient place for
        developers to handle what happens during every request per their
        application needs.
                
        """
        
class RequestHandler(meta.MetaMixin):
    """
    Generic class that handles HTTP requests.
    
    """
    class Meta:
        baseurl = None
        debug = False
        serialization = serialization.JsonSerializationHandler
        serialize = False
        deserialize = True
    
    extra_params = {}
    extra_url_params = {}
    extra_headers= {}
    
    def __init__(self, **kw):
        super(RequestHandler, self).__init__(**kw)
        
        self._meta.baseurl = self._meta.baseurl.rstrip('/')
        
        if os.environ.has_key('DREST_DEBUG') and \
           os.environ['DREST_DEBUG'] in [1, '1']:
            self._meta.debug = True
        
        if not self._meta.serialization:
            self._meta.serialize = False
            self._meta.deserialize = False
            
        else:
            serialization.validate(self._meta.serialization)
            self._serialization = self._meta.serialization()
            headers = self._serialization.get_headers()
            for key in headers:
                self.extra_headers[key] = headers[key]
                   
    def add_param(self, key, value):
        self.extra_params[key] = value
    
    def add_url_param(self, key, value):
        self.extra_url_params[key] = value
        
    def add_header(self, key, value):
        self.extra_headers[key] = value
       
    def _make_request(self, url, method, payload={}, headers={}): 
        try:
            http = Http()
            return http.request(url, method, payload, headers=headers)
        except socket.error as e:
            raise exc.dRestAPIError(e.args[1])
            
    def request(self, method, path, params={}, headers={}):
        """
        Make a call to a resource based on path, and parameters.
    
        Required Arguments:
    
            method 
                One of HEAD, GET, POST, DELETE.
                
            path
                The path to the resource, after baseurl.
            
                
        Optional Arguments:
        
            params
                Dictionary of keyword arguments.
            
        """        
        path = path.lstrip('/').rstrip('/')
        for key in self.extra_params:
            params[key] = self.extra_params[key]
        
        for key in self.extra_headers:
            headers[key] = self.extra_headers[key]
                
        if path == '':
            url = self._meta.baseurl
        else:
            url = "%s/%s/" % (self._meta.baseurl, path)

        if method == 'GET':
            for key in params:
                self.add_url_param(key, params[key])
                
        if self.extra_url_params:
            url = "%s?%s" % (url, urlencode(self.extra_url_params))
            
        if self._meta.debug:
            print '---'
            print 'DREST_DEBUG: method=%s url=%s params=%s headers=%s' % \
                   (method, url, params, headers)
            print '---'
            
        if self._meta.serialize: 
            payload = self._serialization.serialize(params)
            response, content = self._make_request(url, method, payload,
                                                   headers=headers)
        else:
            payload = urlencode(params)
            response, content = self._make_request(url, method, payload,
                                                   headers=headers)
            response.unserialized_content = content

        if self._meta.deserialize:
            response.serialized_content = content
            content = self._serialization.deserialize(content)
    
        response.method = method
        response.payload = payload
        response.url = url

        self.handle_response(response, content)
        return response, content
    
    def handle_response(self, response, content):
        """
        A simple wrapper to handle the response.  By default raises 
        exc.dRestRequestError if the response code is within 400-499, or 500.
        
        Required Arguments:
        
            response
                The response object.
                
            content
                The response content.
        """
        if (400 <= response.status <=499) or (response.status == 500):
            msg = "Received HTTP Code %s - %s" % (
                   response.status, 
                   httplib.responses[int(response.status)])
            raise exc.dRestRequestError(
                msg, response=response, content=content
                )

        return (response, content)

class TastyPieRequestHandler(RequestHandler):
    """
    This class implements the IRequest interface, specifically tailored for
    interfacing with `TastyPie <http://django-tastypie.readthedocs.org/en/latest>`_.
    
    """
    def __init__(self, **kw):
        super(TastyPieRequestHandler, self).__init__(**kw)
                