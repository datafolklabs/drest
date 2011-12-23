
import os
import httplib
import socket
from httplib2 import Http
from urllib import urlencode
from urllib2 import urlopen

from drest import exc, interface

def validate(obj):
    """Validates a handler implementation against the ISerialize interface."""
    members = [
        'setup',
        'add_param',
        'add_header',
        'auth',
        'request',
        'extra_params',
        'extra_headers',
        'serialization_handler',
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
    
    extra_params = interface.Attribute('Parameters to pass with each request.')
    auth_params = interface.Attribute('Auth parameters to attach to the url.')
    extra_headers = interface.Attribute('Headers to pass with each request.')
    serialization_handler = interface.Attribute('Serialization handler object')
    #response_handler = interface.Attribute('Response handler object')
    
    def setup(baseurl, **kw):
        """
        The setup function is called during connection initialization and
        must 'setup' the handler object making it ready for the connection
        or the application to make further calls to it.
        
        Required Arguments:
        
            baseurl
                The base url of the upstream API.
                
        Optional Arguments:
        
            serialize
                Whether or not to serialize the request parameters.
            
            deserialize
                Whether or not to deserialize the response content.
            
            serialization_handler
                The class with which to handle serialization.
                
        Returns: n/a
        
        """
    
    def add_param(key, value):
        """
        Add extra parameters to pass along with the url for *every* request.
        
        Required Arguments:
        
            key
                The key of the parameter to add.
            
            value
                The value of the parameter to add.
                
        """
        
    def add_param(key, value):
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
        
class RequestHandler(object):
    extra_params = {}
    auth_params = {}
    extra_headers= {}
    serialization_handler = None
    
    def __init__(self):
        self.baseurl = None
        self.debug = False
        self.serialize = False
        self.deserialize = False
        
    def setup(self, baseurl, **kw):
        self.baseurl = baseurl.rstrip('/')
        self.serialization_handler = kw.get('serialization_handler', None)
        
        if self.serialization_handler:
            self.serialize = kw.get('serialize', True)
            self.deserialize = kw.get('deserialize', True)
        
        if os.environ.has_key('DREST_DEBUG') and \
           os.environ['DREST_DEBUG'] in [1, '1']:
            self.debug = True
            
        if self.serialize and self.serialization_handler:
            headers = self.serialization_handler.get_headers()
            for key in headers:
                self.extra_headers[key] = headers[key]
                
    def add_param(self, key, value):
        self.extra_params[key] = value
    
    def add_header(self, key, value):
        self.extra_headers[key] = value
            
    def auth(self, **kw):
        """
        In this implementation, we simply add any keywords passed to 
        self.auth_params so that they are passed along with each request.
        For example, auth(user='john.doe', api_key='XXXXX').
                
        """
        for key in kw:
            self.auth_params = kw
       
    def _make_request(self, url, method, payload={}, headers={}): 
        try:
            http = Http()
            return http.request(url, method, payload, headers=headers)
        except socket.error as e:
            raise exc.dRestConnectionError(e.args[1])
            
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
        path = path.strip('/')
        
        for key in self.extra_params:
            params[key] = self.extra_params[key]
        
        for key in self.extra_headers:
            headers[key] = self.extra_headers[key]
                
        url = "%s/%s/" % (self.baseurl, path)
        if self.auth_params:
            url = "%s?%s" % (url, urlencode(self.auth_params))
            
        if self.debug:
            print '---'
            print 'DREST_DEBUG: method=%s url=%s params=%s headers=%s' % \
                   (method, url, params, headers)
            print '---'
            
        if self.serialize and self.serialization_handler: 
            payload = self.serialization_handler.dump(params)
            response, content = self._make_request(url, method, payload,
                                                   headers=headers)
        else:
            # Here we clean up the params a bit.  Nosne type doesn't transfer over 
            # HTTP_POST, and if the param is a python list we need to break that
            # out into multiple params with the same name.  Therefore, we convert
            # the dict into a list of tuples.
            tup_list = []    
            for key in params:
                if params[key] == None:
                    params[key] = ''
                    tup_list.append((key, params[key]))
                elif type(params[key]) == list:
                    for i in params[key]:
                        tup_list.append((key, i))
                else:
                    tup_list.append((key, params[key]))
                
            payload = urlencode(tup_list)
        
            if method == 'GET':
                url = "%s?%s" % (url, payload)
                
            response, content = self._make_request(url, method, payload,
                                                   headers=headers)
            response.unserialized_content = content

        if self.serialize and self.serialization_handler:
            response.unserialized_content = content
            content = self.serialization_handler.load(content)
    
        response.method = method
        response.payload = payload
        response.url = url

        self.handle_response(response, content)
        return response, content
    
    def handle_response(self, response, content):
        """
        A simple wrapper to handle the response.  Be default raises 
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