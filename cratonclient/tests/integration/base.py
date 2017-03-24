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

import betamax
from betamax_matchers import json_body
from keystoneauth1.fixture import keystoneauth_betamax as ksabetamax

from cratonclient import auth
from cratonclient import exceptions
from cratonclient.tests import base
from cratonclient.v1 import client

# NOTE(sigmavirus24): This allows us to use ``'json-body'`` as a matcher below
betamax.Betamax.register_request_matcher(json_body.JSONBodyMatcher)
envget = os.environ.get

CRATON_DEMO_USERNAME = envget('CRATON_DEMO_USERNAME', 'demo')
CRATON_DEMO_TOKEN = envget('CRATON_DEMO_TOKEN', 'demo')
CRATON_DEMO_PROJECT = envget('CRATON_DEMO_PROJECT',
                             'b9f10eca66ac4c279c139d01e65f96b5')
CRATON_ROOT_USERNAME = envget('CRATON_ROOT_USERNAME', 'root')
CRATON_ROOT_TOKEN = envget('CRATON_ROOT_TOKEN', 'root')
CRATON_ROOT_PROJECT = envget('CRATON_ROOT_PROJECT',
                             'b9f10eca66ac4c279c139d01e65f96b5')
CRATON_URL = envget('CRATON_URL', 'http://127.0.0.1:8080/v1')


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
        self.record_mode = envget('BETAMAX_RECORD_MODE', 'once')
        self.url = CRATON_URL
        self.betamax_fixture = self.useFixture(ksabetamax.BetamaxFixture(
            cassette_name=self.cassette_name,
            cassette_library_dir=self.CASSETTE_LIBRARY_DIR,
            record=self.record_mode,
        ))
        self.demo_credentials = {
            'username': CRATON_DEMO_USERNAME,
            'token': CRATON_DEMO_TOKEN,
            'project': CRATON_DEMO_PROJECT,
        }
        self.root_credentials = {
            'username': CRATON_ROOT_USERNAME,
            'token': CRATON_ROOT_TOKEN,
            'project': CRATON_ROOT_PROJECT,
        }

    def assertNotFound(self, func, item_id):
        """Assert that the item referenced by item_id 404s."""
        self.assertRaises(exceptions.NotFound, func, item_id)

    def cleanupHost(self, host):
        """Add a cleanup task for the host."""
        self.addCleanup(self.client.hosts.delete, host.id)
        return host

    def cleanupCloud(self, cloud):
        """Add a cleanup task for the cloud."""
        self.addCleanup(self.client.clouds.delete, cloud.id)
        return cloud

    def cleanupRegion(self, region):
        """Add a cleanup task for the region."""
        self.addCleanup(self.client.regions.delete, region.id)
        return region

    def cleanupCell(self, cell):
        """Add a cleanup task for the cell."""
        self.addCleanup(self.client.cells.delete, cell.id)
        return cell

    def create_client(self, username, token, project):
        """Create a Craton client using Craton Auth."""
        self.session = auth.craton_auth(
            username=username,
            token=token,
            project_id=project,
        )
        self.client = client.Client(self.session, self.url)

    def create_demo_client(self):
        """Set up cratonclient with the demo user."""
        self.create_client(**self.demo_credentials)


with betamax.Betamax.configure() as config:
    config.define_cassette_placeholder(
        '<craton-demo-username>', CRATON_DEMO_USERNAME,
    )
    config.define_cassette_placeholder(
        '<craton-demo-token>', CRATON_DEMO_TOKEN,
    )
    config.define_cassette_placeholder(
        '<craton-demo-project>', CRATON_DEMO_PROJECT,
    )
    config.define_cassette_placeholder(
        '<craton-root-username>', CRATON_ROOT_USERNAME,
    )
    config.define_cassette_placeholder(
        '<craton-root-token>', CRATON_ROOT_TOKEN,
    )
    config.define_cassette_placeholder(
        '<craton-root-project>', CRATON_ROOT_PROJECT,
    )
    config.define_cassette_placeholder(
        '<craton-url>', CRATON_URL,
    )
