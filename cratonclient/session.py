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
from itertools import chain
import logging

from keystoneauth1 import session as ksa_session
from requests import exceptions as requests_exc

import cratonclient
from cratonclient import auth
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
            The session instance to use as an underlying HTTP transport. If
            not provided, we will create a keystoneauth1 Session object.
        :param str username:
            The username of the person authenticating against the API.
        :param str token:
            The authentication token of the user authenticating.
        :param str project_id:
            The user's project id in Craton.
        """
        if session is None:
            _auth = auth.CratonAuth(
                username=username,
                project_id=project_id,
                token=token,
            )
            session = ksa_session.Session(auth=_auth)
        self._session = session
        self._session.user_agent = 'python-cratonclient/{0}'.format(
            cratonclient.__version__)

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
        kwargs.setdefault('endpoint_filter',
                          {'service_type': 'fleet_management'})
        try:
            response = self._session.request(
                method=method,
                url=url,
                **kwargs
            )
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

        if response.status_code >= 400:
            raise exc.error_from(response)

        return response

    def paginate(self, url, items_key, autopaginate=True, nested=False,
                 **kwargs):
        """Make a GET request to a paginated resource.

        If :param:`autopaginate` is set to ``True``, this will automatically
        handle finding and retrieving the next page of items.

        .. code-block:: python

            >>> from cratonclient import session as craton
            >>> session = craton.Session(
            ...     username='demo',
            ...     token='p@##w0rd',
            ...     project_id='84363597-721c-4068-9731-8824692b51bb',
            ... )
            >>> url = 'https://example.com/v1/hosts'
            >>> for response in session.paginate(url, items_key='hosts'):
            ...     print("Received status {}".format(response.status_code))
            ...     print("Received {} items".format(len(items)))

        :param bool autopaginate:
            Determines whether or not this method continues requesting items
            automatically after the first page.
        """
        get_items = True

        while get_items:
            response = self.get(url, **kwargs)
            json_body = response.json()
            if nested:
                items = list(chain(*json_body[items_key].values()))
            else:
                items = json_body[items_key]

            yield response, items

            links = json_body['links']
            url = _find_next_link(links)

            kwargs = {}
            get_items = url and autopaginate and len(items) > 0


def _find_next_link(links):
    for link in links:
        if link['rel'] == 'next':
            return link['href']

    return None
