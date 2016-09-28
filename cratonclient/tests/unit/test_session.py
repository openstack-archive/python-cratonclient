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
"""Session specific unit tests."""
from keystoneauth1 import session as ksa_session

from cratonclient import session
from cratonclient.tests import base


TEST_USERNAME_0 = 'test'
TEST_PROJECT_0 = 1
TEST_TOKEN_0 = 'fake-token'


class TestCratonAuth(base.TestCase):
    """Craton authentication keystoneauth plugin tests."""

    def test_stores_authentication_details(self):
        """Verify that our plugin stores auth details."""
        plugin = session.CratonAuth(username=TEST_USERNAME_0,
                                    project_id=TEST_PROJECT_0,
                                    token=TEST_TOKEN_0)
        self.assertEqual(TEST_USERNAME_0, plugin.username)
        self.assertEqual(TEST_PROJECT_0, plugin.project_id)
        self.assertEqual(TEST_TOKEN_0, plugin.token)

    def test_generates_appropriate_headers(self):
        """Verify we generate the X-Auth-* headers."""
        fake_session = object()
        plugin = session.CratonAuth(username=TEST_USERNAME_0,
                                    project_id=TEST_PROJECT_0,
                                    token=TEST_TOKEN_0)
        self.assertDictEqual(
            {
                'X-Auth-Token': TEST_TOKEN_0,
                'X-Auth-User': TEST_USERNAME_0,
                'X-Auth-Project': '{}'.format(TEST_PROJECT_0),
            },
            plugin.get_headers(fake_session)
        )

    def test_stores_token(self):
        """Verify get_token returns our token."""
        fake_session = object()
        plugin = session.CratonAuth(username=TEST_USERNAME_0,
                                    project_id=TEST_PROJECT_0,
                                    token=TEST_TOKEN_0)

        self.assertEqual(TEST_TOKEN_0, plugin.get_token(fake_session))


class TestSession(base.TestCase):
    """Unit tests for cratonclient's Session abstraction."""

    def test_creates_craton_auth_plugin(self):
        """Verify we default to using keystoneauth plugin auth."""
        craton_session = session.Session(username=TEST_USERNAME_0,
                                         project_id=TEST_PROJECT_0,
                                         token=TEST_TOKEN_0)

        self.assertIsInstance(craton_session._auth, session.CratonAuth)

    def test_creates_keystoneauth_session(self):
        """Verify we default to keystoneauth sessions and semantics."""
        craton_session = session.Session(username=TEST_USERNAME_0,
                                         project_id=TEST_PROJECT_0,
                                         token=TEST_TOKEN_0)

        self.assertIsInstance(craton_session._session, ksa_session.Session)

    def test_will_use_the_existing_session(self):
        """Verify we don't overwrite an existing session object."""
        ksa_session_obj = ksa_session.Session()
        craton_session = session.Session(session=ksa_session_obj)

        self.assertIs(ksa_session_obj, craton_session._session)
