# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Exception classes and logic for cratonclient."""


class ClientException(Exception):
    """Base exception class for all exceptions in cratonclient."""

    message = None

    def __init__(self, message=None):
        """Initialize our exception instance with our class level message."""
        if message is None:
            if self.message is None:
                message = self.__class__.__name__
            else:
                message = self.message
        super(ClientException, self).__init__(message)


class UnableToAuthenticate(ClientException):
    """There are insufficient parameters for authentication."""

    message = "Some of the parameters required to authenticate were missing."""


class Timeout(ClientException):
    """Catch-all class for connect and read timeouts from requests."""

    message = 'Request timed out'

    def __init__(self, message=None, **kwargs):
        """Initialize our Timeout exception.

        This takes an optional keyword-only argument of
        ``original_exception``.
        """
        self.original_exception = kwargs.pop('exception', None)
        super(Timeout, self).__init__(message)


class HTTPError(ClientException):
    """Base exception class for all HTTP related exceptions in."""

    message = "An error occurred while talking to the remote server."
    status_code = None

    def __init__(self, message=None, **kwargs):
        """Initialize our HTTPError instance.

        Optional keyword-only arguments include:

        - response: for the response generating the error
        - original_exception: in the event that this is a requests exception
          that we are re-raising.
        """
        self.response = kwargs.pop('response', None)
        self.original_exception = kwargs.pop('exception', None)
        self.status_code = (self.status_code
                            or getattr(self.response, 'status_code', None))
        super(HTTPError, self).__init__(message)

    @property
    def status_code(self):
        """Shim to provide a similar API to other OpenStack clients."""
        return self.status_code

    @status_code.setter
    def status_code(self, code):
        self.status_code = code


class CommandError(ClientException):
    """Client command was invalid or failed."""

    message = "The command used was invalid or caused an error."""


class ConnectionFailed(HTTPError):
    """Connecting to the server failed."""

    message = "An error occurred while connecting to the server."""


class HTTPClientError(HTTPError):
    """Base exception for client side errors (4xx status codes)."""

    message = "Something went wrong with the request."


class BadRequest(HTTPClientError):
    """Client sent a malformed request."""

    status_code = 400
    message = "The request sent to the server was invalid."


class Unauthorized(HTTPClientError):
    """Client is unauthorized to access the resource in question."""

    status_code = 401
    message = ("The user has either provided insufficient parameters for "
               "authentication or is not authorized to access this resource.")


class Forbidden(HTTPClientError):
    """Client is forbidden to access the resource."""

    status_code = 403
    message = ("The user was unable to access the resource because they are "
               "forbidden.")


class NotFound(HTTPClientError):
    """Resource could not be found."""

    status_code = 404
    message = "The requested resource was not found."""


class MethodNotAllowed(HTTPClientError):
    """The request method is not supported."""

    status_code = 405
    message = "The method used in the request is not supported."


class NotAcceptable(HTTPClientError):
    """The requested resource can not respond with acceptable content.

    Based on the Accept headers specified by the client, the resource can not
    generate content that is an acceptable content-type.
    """

    status_code = 406
    message = "The resource can not return acceptable content."


class ProxyAuthenticationRequired(HTTPClientError):
    """The client must first authenticate itself with the proxy."""

    status_code = 407
    message = "The client must first authenticate itself with a proxy."


class Conflict(HTTPClientError):
    """The request presents a conflict."""

    status_code = 409
    message = "The request could not be processed due to a conflict."


class Gone(HTTPClientError):
    """The requested resource is no longer available.

    The resource requested is no longer available and will not be available
    again.
    """

    status_code = 410
    message = ("The resource requested is no longer available and will not be"
               " available again.")


class LengthRequired(HTTPClientError):
    """The request did not specify a Content-Length header."""

    status_code = 411
    message = ("The request did not contain a Content-Length header but one"
               " was required by the resource.")


class PreconditionFailed(HTTPClientError):
    """The server failed to meet one of the preconditions in the request."""

    status_code = 412
    message = ("The server failed to meet one of the preconditions in the "
               "request.")


class RequestEntityTooLarge(HTTPClientError):
    """The request is larger than the server is willing or able to process."""

    status_code = 413
    message = ("The request is larger than the server is willing or able to "
               "process.")


class RequestUriTooLong(HTTPClientError):
    """The URI provided was too long for the server to process."""

    status_code = 414
    message = "The URI provided was too long for the server to process."


class UnsupportedMediaType(HTTPClientError):
    """The request entity has a media type which is unsupported."""

    status_code = 415
    message = ("The request entity has a media type which is unsupported by "
               "the server or resource.")


class RequestedRangeNotSatisfiable(HTTPClientError):
    """The requestor wanted a range but the server was unable to provide it."""

    status_code = 416
    message = ("The requestor wanted a range but the server was unable to "
               "provide it.")


class UnprocessableEntity(HTTPClientError):
    """There were semantic errors in the request."""

    status_code = 422
    message = ("The request is of a valid content-type and structure but "
               "semantically invalid.")


_4xx_classes = [
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    ProxyAuthenticationRequired,
    Conflict,
    Gone,
    LengthRequired,
    PreconditionFailed,
    RequestEntityTooLarge,
    RequestUriTooLong,
    UnsupportedMediaType,
    RequestedRangeNotSatisfiable,
    UnprocessableEntity,
]
_4xx_codes = {cls.status_code: cls for cls in _4xx_classes}


class HTTPServerError(HTTPError):
    """The server encountered an error it could not recover from."""

    message = "HTTP Server-side Error"


class InternalServerError(HTTPServerError):
    """The server encountered an error it could not recover from."""

    status_code = 500
    message = ("There was an internal server error that could not be recovered"
               " from.")


_5xx_classes = [
    InternalServerError,
    # NOTE(sigmavirus24): Allow for future expansion
]
_5xx_codes = {cls.status_code: cls for cls in _5xx_classes}


def error_from(response):
    """Find an error code that matches a response status_code."""
    if 400 <= response.status_code < 500:
        cls = _4xx_codes.get(response.status_code, HTTPClientError)
    elif 500 <= response.status_code < 600:
        cls = _5xx_codes.get(response.status_code, HTTPServerError)
    else:
        cls = HTTPError

    return cls(response=response)
