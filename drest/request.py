
import os
from httplib2 import Http
from urllib import urlencode
from urllib2 import urlopen

from drest import exc

class HTTPRequestHandler(object):
    def __init__(self):
        self.baseurl = None
        self.debug = False
        self.extra_params = {}
        self.extra_headers= {}
        
    def setup(self, baseurl):
        self.baseurl = baseurl.rstrip('/')
        
        if os.environ.has_key('DREST_DEBUG') and \
           os.environ['DREST_DEBUG'] == '1':
            self.debug = True
            
    def add_param(self, key, value):
        self.extra_params[key] = value
    
    def add_header(self, key, value):
        self.extra_headers[key] = value
            
    def auth(self, **kw):
        """
        In this implementation, we simply add any keywords passed to 
        self.extra_params so that they are passed along with each request.
        For example, auth(user='john.doe', api_key='XXXXX').
                
        """
        for key in kw:
            self.add_param(key, kw[key])
        
    def request(self, method, path, params={}):
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
        path = path.lstrip('/')
        
        for key in self.extra_params:
            params[key] = self.extra_params[key]
        
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
                
        url = "%s/%s" % (self.baseurl, path)
        data = urlencode(tup_list)
        
        if method == 'GET':
            url = "%s/?%s" % (url, data)
            
        if self.debug:
            print 'DREST_DEBUG: %s?%s' % (url, data)
            
        http = Http()                
        response, content = http.request(url, method, data,
                                         headers=self.extra_headers)
        if len(content) == 0:
            content = '{}'
            
        return response, content
        