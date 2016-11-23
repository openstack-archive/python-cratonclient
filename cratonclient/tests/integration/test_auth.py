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
"""Integration tests for the cratonclient.auth module."""
from oslo_utils import uuidutils

from keystoneauth1.identity.v3 import password as ksa_password
from keystoneauth1 import session as ksa_session

from cratonclient import auth
from cratonclient import session
from cratonclient.tests import base

PROJECT_ID = uuidutils.generate_uuid()


class TestAuth(base.TestCase):
    """Integration tests for the auth module functions."""

    def test_craton_auth_configures_craton_session(self):
        """Verify the configuration of a cratonclient Session."""
        new_session = auth.craton_auth(
            username='demo',
            token='demo',
            project_id=PROJECT_ID,
        )

        self.assertIsInstance(new_session, session.Session)

        keystone_session = new_session._session
        self.assertIsInstance(keystone_session, ksa_session.Session)
        self.assertIsInstance(keystone_session.auth, auth.CratonAuth)

    def test_keystone_auth_configures_craton_session(self):
        """Verify the configuration of a cratonclient Session."""
        new_session = auth.keystone_auth(
            auth_url='https://identity.openstack.org/v3',
            username='admin',
            password='adminPassword',
            project_id=PROJECT_ID,
            project_domain_name='Default',
            user_domain_name='Default',
        )

        self.assertIsInstance(new_session, session.Session)

        keystone_session = new_session._session
        self.assertIsInstance(keystone_session, ksa_session.Session)
        self.assertIsInstance(keystone_session.auth, ksa_password.Password)
