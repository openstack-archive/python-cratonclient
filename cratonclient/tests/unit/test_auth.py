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
"""Unit tests for the cratonclient.auth module."""
import mock

from oslo_utils import uuidutils

from cratonclient import auth
from cratonclient.tests import base

USERNAME = 'test'
TOKEN = 'fake-token'
PROJECT_ID = uuidutils.generate_uuid()


class TestCreateSessionWith(base.TestCase):
    """"Tests for the create_session_with function."""

    def setUp(self):
        """Set up mocks to test the create_session_with function."""
        super(TestCreateSessionWith, self).setUp()
        self._session_mock = mock.patch('cratonclient.session.Session')
        self.session_class = self._session_mock.start()
        self.addCleanup(self._session_mock.stop)

        self._ksa_session_mock = mock.patch('keystoneauth1.session.Session')
        self.ksa_session_class = self._ksa_session_mock.start()
        self.addCleanup(self._ksa_session_mock.stop)

    def test_creates_sessions(self):
        """Verify we create cratonclient and keystoneauth Sesssions."""
        auth_plugin = mock.Mock()
        auth.create_session_with(auth_plugin, True)

        self.ksa_session_class.assert_called_once_with(
            auth=auth_plugin,
            verify=True,
        )
        self.session_class.assert_called_once_with(
            session=self.ksa_session_class.return_value
        )


class TestCratonAuth(base.TestCase):
    """Tests for the craton_auth function."""

    def setUp(self):
        """Set up mocks to test the craton_auth function."""
        super(TestCratonAuth, self).setUp()
        self._create_session_with_mock = mock.patch(
            'cratonclient.auth.create_session_with'
        )
        self.create_session_with = self._create_session_with_mock.start()
        self.addCleanup(self._create_session_with_mock.stop)

        self._craton_auth_mock = mock.patch('cratonclient.auth.CratonAuth')
        self.craton_auth_class = self._craton_auth_mock.start()
        self.addCleanup(self._craton_auth_mock.stop)

    def test_creates_craton_auth_ksa_plugin(self):
        """Verify we create a new instance of CratonAuth."""
        auth.craton_auth(
            username='demo',
            token='demo',
            project_id=PROJECT_ID,
        )

        self.craton_auth_class.assert_called_once_with(
            username='demo',
            token='demo',
            project_id=PROJECT_ID,
        )

    def test_calls_create_session_with(self):
        """Verify we call create_session_with using the right parameters."""
        auth.craton_auth(
            username='demo',
            token='demo',
            project_id=PROJECT_ID,
            verify=False,
        )

        self.create_session_with.assert_called_once_with(
            self.craton_auth_class.return_value, False
        )


class TestKeystoneAuth(base.TestCase):
    """Tests for the keystone_auth function."""

    def setUp(self):
        """Set up mocks to test the keystone_auth function."""
        super(TestKeystoneAuth, self).setUp()
        self._create_session_with_mock = mock.patch(
            'cratonclient.auth.create_session_with'
        )
        self.create_session_with = self._create_session_with_mock.start()
        self.addCleanup(self._create_session_with_mock.stop)

        self._ksa_password_mock = mock.patch(
            'keystoneauth1.identity.v3.password.Password'
        )
        self.ksa_password_class = self._ksa_password_mock.start()
        self.addCleanup(self._ksa_password_mock.stop)

    def test_creates_ksa_password_plugin(self):
        """Verify we create a Password keystoneauth plugin."""
        auth.keystone_auth(
            auth_url='https://identity.openstack.org/v3',
            username='admin',
            password='adminPassword',
            project_name='admin',
            project_domain_name='Default',
            user_domain_name='Default',
        )

        self.ksa_password_class.assert_called_once_with(
            auth_url='https://identity.openstack.org/v3',
            username='admin',
            password='adminPassword',
            project_name='admin',
            project_domain_name='Default',
            user_domain_name='Default',
            project_id=None,
            project_domain_id=None,
            user_domain_id=None,
        )

    def test_calls_create_session_with(self):
        """Verify we call create_session_with using the right parameters."""
        auth.keystone_auth(
            auth_url='https://identity.openstack.org/v3',
            username='admin',
            password='adminPassword',
            project_name='admin',
            project_domain_name='Default',
            user_domain_name='Default',
            verify=False,
        )

        self.create_session_with.assert_called_once_with(
            self.ksa_password_class.return_value, False
        )


class TestCratonAuthPlugin(base.TestCase):
    """Craton authentication keystoneauth plugin tests."""

    def test_stores_authentication_details(self):
        """Verify that our plugin stores auth details."""
        plugin = auth.CratonAuth(
            username=USERNAME,
            project_id=PROJECT_ID,
            token=TOKEN,
        )
        self.assertEqual(USERNAME, plugin.username)
        self.assertEqual(PROJECT_ID, plugin.project_id)
        self.assertEqual(TOKEN, plugin.token)

    def test_generates_appropriate_headers(self):
        """Verify we generate the X-Auth-* headers."""
        fake_session = object()
        plugin = auth.CratonAuth(
            username=USERNAME,
            project_id=PROJECT_ID,
            token=TOKEN,
        )
        self.assertDictEqual(
            {
                'X-Auth-Token': TOKEN,
                'X-Auth-User': USERNAME,
                'X-Auth-Project': '{}'.format(PROJECT_ID),
            },
            plugin.get_headers(fake_session)
        )

    def test_stores_token(self):
        """Verify get_token returns our token."""
        fake_session = object()
        plugin = auth.CratonAuth(
            username=USERNAME,
            project_id=PROJECT_ID,
            token=TOKEN,
        )

        self.assertEqual(TOKEN, plugin.get_token(fake_session))
