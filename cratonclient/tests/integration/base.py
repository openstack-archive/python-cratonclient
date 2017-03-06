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
"""Module containing the base logic for cratonclient integration tests."""
import os

from keystoneauth1.fixture import keystoneauth_betamax as ksabetamax

from cratonclient import auth
from cratonclient.tests import base
from cratonclient.v1 import client


class BetamaxTestCase(base.TestCase):
    """This sets up Betamax with Keystoneauth1 fixture for integration tests.

    This relies on existing keystoneauth1 integration with the Betamax library
    to make recording integration tests easier.
    """

    CASSETTE_LIBRARY_DIR = 'cratonclient/tests/cassettes/'

    def generate_cassette_name(self):
        """Generate a cassette name for the current test."""
        full_test_name = self.id()
        module, test_class, test_method = full_test_name.rsplit('.', 2)
        return test_class + '-' + test_method

    def setUp(self):
        """Set up betamax fixture for cratonclient."""
        super(BetamaxTestCase, self).setUp()
        self.cassette_name = self.generate_cassette_name()
        self.record_mode = os.environ.get('BETAMAX_RECORD_MODE', 'once')
        self.url = os.environ.get('CRATON_URL', 'http://127.0.0.1:8080')
        self.betamax_fixture = self.useFixture(ksabetamax.BetamaxFixture(
            cassette_name=self.cassette_name,
            cassette_library_dir=self.CASSETTE_LIBRARY_DIR,
            record=self.record_mode,
        ))

    def create_client(self, username, token, project):
        self.session = auth.craton_auth(
            username=username,
            token=token,
            project_id=project,
        )
        self.client = client.Client(self.session, self.url)

    def create_demo_client(self):
        """Set up cratonclient with the demo user."""
        self.create_client(
            username='demo',
            token='demo',
            project='b9f10eca66ac4c279c139d01e65f96b4',
        )
