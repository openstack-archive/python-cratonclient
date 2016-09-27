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
"""Craton-specific session details."""
import logging

from oslo_utils import encodeutils
from oslo_utils import strutils
import requests
from requests import exceptions as requests_exc
import six

import cratonclient
from cratonclient import exceptions as exc

LOG = logging.getLogger(__name__)


class Session(object):
    """Management class to allow different types of sessions to be used.

    If an instance of Craton is deployed with Keystone Middleware, this allows
    for a keystoneauth session to be used so authentication will happen
    immediately.
    """

    def __init__(self, session=None, username=None, token=None,
                 project_id=None):
        """Initialize our Session.

        :param session:
            The session instance (either keystoneauth1's session or requests
            Session) to use as an underlying HTTP transport. If not provided,
            we will create a requests Session object.
        :param str username:
            The username of the person authenticating against the API.
        :param str token:
            The authentication token of the user authenticating.
        :param str project_id:
            The user's project id in Craton.
        """
        if session is None:
            session = requests.Session()
        self.project_id = project_id
        self._session = session
        self._session.headers['X-Auth-User'] = username
        self._session.headers['X-Auth-Project'] = str(project_id)
        self._session.headers['X-Auth-Token'] = token

        craton_version = 'python-cratonclient/{0} '.format(
            cratonclient.__version__)
        old_user_agent = self._session.headers['User-Agent']

        self._session.headers['User-Agent'] = craton_version + old_user_agent
        self._session.headers['Accept'] = 'application/json'

    def delete(self, url, **kwargs):
        """Make a DELETE request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.delete('http://example.com')
        """
        return self.request('DELETE', url, **kwargs)

    def get(self, url, **kwargs):
        """Make a GET request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.get('http://example.com')
        """
        return self.request('GET', url, **kwargs)

    def head(self, url, **kwargs):
        """Make a HEAD request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.head('http://example.com')
        """
        return self.request('HEAD', url, **kwargs)

    def options(self, url, **kwargs):
        """Make an OPTIONS request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.options('http://example.com')
        """
        return self.request('OPTIONS', url, **kwargs)

    def post(self, url, **kwargs):
        """Make a POST request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.post(
            ...     'http://example.com',
            ...     data=b'foo',
            ...     headers={'Content-Type': 'text/plain'},
            ... )
        """
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """Make a PUT request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.put(
            ...     'http://example.com',
            ...     data=b'foo',
            ...     headers={'Content-Type': 'text/plain'},
            ... )
        """
        return self.request('PUT', url, **kwargs)

    def patch(self, url, **kwargs):
        """Make a PATCH request with url and optional parameters.

        See the :meth:`Session.request` documentation for more details.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.put(
            ...     'http://example.com',
            ...     data=b'foo',
            ...     headers={'Content-Type': 'text/plain'},
            ... )
            >>> response = session.patch(
            ...     'http://example.com',
            ...     data=b'bar',
            ...     headers={'Content-Type': 'text/plain'},
            ... )
        """
        return self.request('PATCH', url, **kwargs)

    def request(self, method, url, **kwargs):
        """Make a request with a method, url, and optional parameters.

        See also: python-requests.org for documentation of acceptable
        parameters.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@$$w0rd',
            ...     project_id='1',
            ... )
            >>> response = session.request('GET', 'http://example.com')
        """
        self._http_log_request(method=method,
                               url=url,
                               data=kwargs.get('data'),
                               headers=kwargs.get('headers', {}).copy())
        try:
            response = self._session.request(method=method,
                                             url=url,
                                             **kwargs)
        except requests_exc.HTTPError as err:
            raise exc.HTTPError(exception=err, response=err.response)
        # NOTE(sigmavirus24): The ordering of Timeout before ConnectionError
        # is important on requests 2.x. The ConnectTimeout exception inherits
        # from both ConnectionError and Timeout. To catch both connect and
        # read timeouts similarly, we need to catch this one first.
        except requests_exc.Timeout as err:
            raise exc.Timeout(exception=err)
        except requests_exc.ConnectionError as err:
            raise exc.ConnectionFailed(exception=err)

        self._http_log_response(response)
        if response.status_code >= 400:
            raise exc.error_from(response)

        return response

    def _http_log_request(self, url, method=None, data=None,
                          headers=None, logger=LOG):
        if not logger.isEnabledFor(logging.DEBUG):
            # NOTE(morganfainberg): This whole debug section is expensive,
            # there is no need to do the work if we're not going to emit a
            # debug log.
            return

        string_parts = ['REQ: curl -g -i']

        # NOTE(jamielennox): None means let requests do its default validation
        # so we need to actually check that this is False.
        if self.verify is False:
            string_parts.append('--insecure')
        elif isinstance(self.verify, six.string_types):
            string_parts.append('--cacert "%s"' % self.verify)

        if method:
            string_parts.extend(['-X', method])

        string_parts.append(url)

        if headers:
            for header in six.iteritems(headers):
                string_parts.append('-H "%s: %s"'
                                    % self._process_header(header))

        if data:
            string_parts.append("-d '%s'" % data)
        try:
            logger.debug(' '.join(string_parts))
        except UnicodeDecodeError:
            logger.debug("Replaced characters that could not be decoded"
                         " in log output, original caused UnicodeDecodeError")
            string_parts = [
                encodeutils.safe_decode(
                    part, errors='replace') for part in string_parts]
            logger.debug(' '.join(string_parts))

    def _http_log_response(self, response, logger=LOG):
        if not logger.isEnabledFor(logging.DEBUG):
            return

        string_parts = [
            'RESP:',
            '[%s]' % response.status_code
        ]
        for header in six.iteritems(response.headers):
            string_parts.append('%s: %s' % self._process_header(header))
        if response.text:
            string_parts.append('\nRESP BODY: %s\n' %
                                strutils.mask_password(response.text))

        logger.debug(' '.join(string_parts))
