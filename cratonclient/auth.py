# Copyright (c) 2016 Rackspace
#
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
"""Module that simplifies and unifies authentication for Craton."""
from keystoneauth1.identity.v3 import password as ksa_password
from keystoneauth1 import plugin
from keystoneauth1 import session as ksa_session

from cratonclient import exceptions as exc


def craton_auth(username, token, project_id, verify=True):
    """Configure a cratonclient Session to authenticate to Craton.

    This will create, configure, and return a Session object that will use
    Craton's built-in authentication method.

    :param str username:
        The username with which to authentiate against the API.
    :param str token:
        The token with which to authenticate against the API.
    :param str project_id:
        The project ID that the user belongs to.
    :param bool verify:
        (Optional) Whether or not to verify HTTPS certificates provided by the
        server. Default: True
    :returns:
        Configured cratonclient session.
    :rtype:
        cratonclient.session.Session

    Example:

    .. code-block:: python

        from cratonclient import auth
        from cratonclient.v1 import client

        craton = client.Client(session=auth.craton_auth(
            username='demo',
            token='demo',
            project_id='b9f10eca66ac4c279c139d01e65f96b4',
        ))

    """
    auth_plugin = CratonAuth(
        username=username,
        token=token,
        project_id=project_id,
    )
    return create_session_with(auth_plugin, verify)


def keystone_auth(auth_url, username, password, verify=True,
                  project_name=None, project_id=None,
                  project_domain_name=None, project_domain_id=None,
                  user_domain_name=None, user_domain_id=None,
                  **auth_parameters):
    r"""Configure a cratonclient Session to authenticate with Keystone.

    This will create, configure, and return a Session using thet appropriate
    Keystone authentication plugin to be able to communicate and authenticate
    to Craton.

    .. note::

        Presently, this function supports only V3 Password based
        authentication to Keystone. We also do not validate that you specify
        required attributes. For example, Keystone will require you provide
        ``project_name`` or ``project_id`` but we will not enforce whether or
        not you've specified one.

    :param str auth_url:
        The URL of the Keystone instance to authenticate to.
    :param str username:
        The username with which we will authenticate to Keystone.
    :param str password:
        The password used to authenticate to Keystone.
    :param str project_name:
        (Optional) The name of the project the user belongs to.
    :param str project_id:
        (Optional) The ID of the project the user belongs to.
    :param str project_domain_name:
        (Optional) The name of the project's domain.
    :param str project_domain_id:
        (Optional) The ID of the project's domain.
    :param str user_domain_name:
        (Optional) The name of the user's domain.
    :param str user_domain_id:
        (Optional) The ID of the user's domain.
    :param bool verify:
        (Optional) Whether or not to verify HTTPS certificates provided by the
        server. Default: True
    :param \*\*auth_parameters:
        Any extra authentication parameters used to authenticate to Keystone.
        See the Keystone documentation for usage of:
        - ``trust_id``
        - ``domain_id``
        - ``domain_name``
        - ``reauthenticate``
    :returns:
        Configured cratonclient session.
    :rtype:
        cratonclient.session.Session

    Example:

    .. code-block:: python

        from cratonclient import auth
        from cratonclient.v1 import client

        craton = client.Client(session=auth.keystone_auth(
            auth_url='https://keystone.cloud.org/v3',
            username='admin',
            password='s3cr373p@55w0rd',
            project_name='admin',
            project_domain_name='Default',
            user_domain_name='Default',
        ))
    """
    password_auth = ksa_password.Password(
        auth_url=auth_url,
        username=username,
        password=password,
        project_id=project_id,
        project_name=project_name,
        project_domain_id=project_domain_id,
        project_domain_name=project_domain_name,
        user_domain_id=user_domain_id,
        user_domain_name=user_domain_name,
        **auth_parameters
    )
    return create_session_with(password_auth, verify)


def create_session_with(auth_plugin, verify):
    """Create a cratonclient Session with the specified auth and verify values.

    :param auth_plugin:
        The authentication plugin to use with the keystoneauth1 Session
        object.
    :type auth_plugin:
        keystoneauth1.plugin.BaseAuthPlugin
    :param bool verify:
        Whether or not to verify HTTPS certificates provided by the server.
    :returns:
        Configured cratonclient session.
    :rtype:
        cratonclient.session.Session
    """
    from cratonclient import session
    return session.Session(session=ksa_session.Session(
        auth=auth_plugin,
        verify=verify,
    ))


class CratonAuth(plugin.BaseAuthPlugin):
    """Custom authentication plugin for keystoneauth1.

    This is specifically for the case where we're not using Keystone for
    authentication.
    """

    def __init__(self, username, project_id, token):
        """Initialize our craton authentication class."""
        self.username = username
        self.project_id = project_id
        self.token = token

    def get_token(self, session, **kwargs):
        """Return our token."""
        return self.token

    def get_headers(self, session, **kwargs):
        """Return the craton authentication headers."""
        headers = super(CratonAuth, self).get_headers(session, **kwargs)
        if headers is None:
            # NOTE(sigmavirus24): This means that the token must be None. We
            # should not allow this to go further. We're using built-in Craton
            # authentication (not authenticating against Keystone) so we will
            # be unable to authenticate.
            raise exc.UnableToAuthenticate()

        headers['X-Auth-User'] = self.username
        headers['X-Auth-Project'] = '{}'.format(self.project_id)
        return headers
