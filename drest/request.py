
import os
import sys

if sys.version_info[0] < 3:
    import httplib # pragma: no cover
    from urllib import urlencode # pragma: no cover
    from urllib2 import urlopen # pragma: no cover

else:
    from http import client as httplib # pragma: no cover
    from urllib.parse import urlencode # pragma: no cover
    from urllib.request import urlopen # pragma: no cover

import socket
from httplib2 import Http, ServerNotFoundError

from . import exc, interface, meta, serialization, response

def validate(obj):
    """Validates a handler implementation against the IRequest interface."""
    members = [
        'add_param',
        'add_url_param',
        'add_header',
        'make_request',
        'handle_response',
        ]
    metas = [
        'response_handler',
        'serialization_handler',
        'serialize',
        'deserialize',
        ]
    interface.validate(IRequest, obj, members, metas)

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

    def add_param(key, value):
        """
        Add extra parameters to pass along with  *every* request.
        These are passed with the request 'payload' (serialized if a
        serialization handler is enabled).  With GET requests they are
        appended to the URL.

        Required Arguments:

            key
                The key of the parameter to add.

            value
                The value of the parameter to add.

        """

    def add_url_param(key, value):
        """
        Similar to 'add_params', however this function adds extra parameters
        to the url for *every* request.
        These are *not* passed with the request 'payload' (serialized if a
        serialization handler is enabled) except for GET requests.

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

    def make_request(method, path, params=None, headers=None):
        """
        Make a request with the upstream API.

        Required Arguments:

            method
                The HTTP method to request as.  I.e. ['GET', 'POST', 'PUT',
                'DELETE', '...'].

            path
                The of the request url *after* the baseurl.


        Optional Arguments:

            params
                Dictionary of parameters to pass with the request.  These will be serialized
                if configured to serialize.

            headers
                Dictionary of headers to pass to the request.

        """

    def handle_response(response_object):
        """
        Called after the request is made.  This is a convenient place for
        developers to handle what happens during every request per their
        application needs.

        Required Arguments:

            response_object
                The response object created by the request.

        """

class RequestHandler(meta.MetaMixin):
    """
    Generic class that handles HTTP requests.  Uses the Json Serialization
    handler by default, but only 'deserializes' response content.

    Optional Arguments / Meta:

        debug
            Boolean.  Toggle debug console output.  Default: False.

        ignore_ssl_validation
            Boolean.  Whether or not to ignore ssl validation errors.
            Default: False

        response_handler
            An un-instantiated Response Handler class used to return
            responses to the caller.  Default: drest.response.ResponseHandler.

        serialization_handler
            An un-instantiated Serialization Handler class used to
            serialize/deserialize data.
            Default: drest.serialization.JsonSerializationHandler.

        serialize
            Boolean.  Whether or not to serialize data before sending
            requests.  Default: False.

        deserialize
            Boolean.  Whether or not to deserialize data before returning
            the Response object.  Default: True.

        trailing_slash
            Boolean.  Whether or not to append a trailing slash to the
            request url.  Default: True.

        timeout
            The amount of seconds where a request should timeout.
            Default: None

    """
    class Meta:
        debug = False
        ignore_ssl_validation = False
        response_handler = response.ResponseHandler
        serialization_handler = serialization.JsonSerializationHandler
        serialize = False
        deserialize = True
        trailing_slash = True
        allow_get_body = False
        timeout = None

    def __init__(self, **kw):
        super(RequestHandler, self).__init__(**kw)
        self._extra_params = {}
        self._extra_url_params = {}
        self._extra_headers = {}
        self._auth_credentials = ()
        self._http = None

        if 'DREST_DEBUG' in os.environ and \
           os.environ['DREST_DEBUG'] in [1, '1']:
            self._meta.debug = True

        response.validate(self._meta.response_handler)
        if self._meta.serialization_handler:
            serialization.validate(self._meta.serialization_handler)
            self._serialization = self._meta.serialization_handler(**kw)
            headers = self._serialization.get_headers()
            for key in headers:
                self.add_header(key, headers[key])
        else:
            self._meta.serialize = False
            self._meta.deserialize = False

    def _serialize(self, data):
        if self._meta.serialize:
            return self._serialization.serialize(data)
        else:
            return data

    def _deserialize(self, data):
        if self._meta.deserialize:
            return self._serialization.deserialize(data)
        else:
            return data

    def set_auth_credentials(self, user, password):
        """
        Set the authentication user and password that will be used for
        HTTP Basic and Digest Authentication.

        Required Arguments:

            user
                The authentication username.

            password
                That user's password.

        """
        self._auth_credentials = (user, password)
        self._clear_http()

    def add_param(self, key, value):
        """
        Adds a key/value to self._extra_params, which is sent with every
        request.

        Required Arguments:

            key
                The key of the parameter.

            value
                The value of 'key'.

        """
        self._extra_params[key] = value

    def add_url_param(self, key, value):
        """
        Adds a key/value to self._extra_url_params, which is sent with every
        request (in the URL).

        Required Arguments:

            key
                The key of the parameter.

            value
                The value of 'key'.

        """
        self._extra_url_params[key] = value

    def add_header(self, key, value):
        """
        Adds a key/value to self._extra_headers, which is sent with every
        request.

        Required Arguments:

            key
                The key of the parameter.

            value
                The value of 'key'.

        """
        self._extra_headers[key] = value

    def _get_http(self):
        """
        Returns either the existing (cached) httplib2.Http() object, or
        a new instance of one.

        """
        if self._http == None:
            if self._meta.ignore_ssl_validation:
                self._http = Http(disable_ssl_certificate_validation=True,
                                  timeout=self._meta.timeout)
            else:
                self._http = Http(timeout=self._meta.timeout)

            if self._auth_credentials:
                self._http.add_credentials(self._auth_credentials[0],
                                           self._auth_credentials[1])
        return self._http

    def _clear_http(self):
        self._http = None

    def _make_request(self, url, method, payload=None, headers=None):
        """
        A wrapper around httplib2.Http.request.

        Required Arguments:

            url
                The url of the request.

            method
                The method of the request. I.e. 'GET', 'PUT', 'POST', 'DELETE'.

        Optional Arguments:

            payload
                The urlencoded parameters.

            headers
                Additional headers of the request.

        """
        if payload is None:
            if self._meta.serialize:
                payload = self._serialize({})
            else:
                payload = urlencode({})
        if headers is None:
            headers = {}

        try:
            http = self._get_http()
            return http.request(url, method, payload, headers=headers)

        except socket.error as e:
            # Try again just in case there was an issue with the cached _http
            try:
                self._clear_http()
                return self._get_http().request(url, method, payload,
                                                headers=headers)
            except socket.error as e:
                raise exc.dRestAPIError(e)

        except ServerNotFoundError as e:
            raise exc.dRestAPIError(e.args[0])

    def _get_complete_url(self, method, url, params):
        url = "%s%s" % (url.strip('/'), '/' if self._meta.trailing_slash else '')

        if method == 'GET':
            url_params = dict(self._extra_url_params, **params)
        else:
            url_params = self._extra_url_params

        if url_params:
            url = "%s?%s" % (url, urlencode(url_params))

        return url

    def make_request(self, method, url, params=None, headers=None):
        """
        Make a call to a resource based on path, and parameters.

        Required Arguments:

            method
                One of HEAD, GET, POST, PUT, PATCH, DELETE, etc.

            url
                The full url of the request (without any parameters).  Any
                params (with GET method) and self.extra_url_params will be
                added to this url.

        Optional Arguments:

            params
                Dictionary of additional (one-time) keyword arguments for the
                request.

            headers
                Dictionary of additional (one-time) headers of the request.

        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        params = dict(self._extra_params, **params)
        headers = dict(self._extra_headers, **headers)
        url = self._get_complete_url(method, url, params)

        if self._meta.serialize:
            payload = self._serialize(params)
        else:
            payload = urlencode(params)

        if self._meta.debug:
            print('DREST_DEBUG: method=%s url=%s params=%s headers=%s' % \
                   (method, url, payload, headers))


        if method is 'GET' and not self._meta.allow_get_body:
            payload = ''
            if self._meta.debug:
                print("DREST_DEBUG: supressing body for GET request")

        res_headers, data = self._make_request(url, method, payload,
                                               headers=headers)
        unserialized_data = data
        serialized_data = None
        if self._meta.deserialize:
            serialized_data = data
            data = self._deserialize(data)

        return_response = response.ResponseHandler(
            int(res_headers['status']), data, res_headers,
            )

        return self.handle_response(return_response)

    def handle_response(self, response_object):
        """
        A simple wrapper to handle the response.  By default raises
        exc.dRestRequestError if the response code is within 400-499, or 500.
        Must return the original, or modified, response object.

        Required Arguments:

            response_object
                The response object created by the request.

        """
        response = response_object
        if (400 <= response.status <=499) or (response.status == 500):
            msg = "Received HTTP Code %s - %s" % (
                   response.status,
                   httplib.responses[int(response.status)])
            raise exc.dRestRequestError(msg, response=response)
        return response

class TastyPieRequestHandler(RequestHandler):
    """
    This class implements the IRequest interface, specifically tailored for
    interfacing with `TastyPie <http://django-tastypie.readthedocs.org/en/latest>`_.

    See :mod:`drest.request.RequestHandler` for Meta options and usage.

    """
    class Meta:
        serialize = True
        deserialize = True
        serialization_handler  = serialization.JsonSerializationHandler

    def __init__(self, **kw):
        super(TastyPieRequestHandler, self).__init__(**kw)
