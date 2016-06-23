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

"""Tests for `cratonclient.session` module."""
import uuid

import requests

import cratonclient
from cratonclient import session
from cratonclient.tests import base

USERNAME = 'example'
TOKEN = uuid.uuid4().hex
PROJECT_ID = 1


class TestSession(base.TestCase):
    """Test our session class."""

    def test_uses_provided_session(self):
        """Verify that cratonclient does not override the session parameter."""
        requests_session = requests.Session()
        craton = session.Session(session=requests_session)
        self.assertIs(requests_session, craton._session)

    def test_creates_new_session(self):
        """Verify that cratonclient creates a new session."""
        craton = session.Session()
        self.assertIsInstance(craton._session, requests.Session)

    def test_sets_authentication_parameters_as_headers(self):
        """Verify we set auth parameters as headers on the session."""
        requests_session = requests.Session()
        craton = session.Session(
            username=USERNAME,
            token=TOKEN,
            project_id=PROJECT_ID,
        )
        expected_headers = {
            'X-Auth-User': USERNAME,
            'X-Auth-Token': TOKEN,
            'X-Auth-Project': str(PROJECT_ID),
            'User-Agent': 'python-cratonclient/{0} {1}'.format(
                cratonclient.__version__,
                requests_session.headers['User-Agent']),
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json',
        }
        self.assertItemsEqual(expected_headers, craton._session.headers)
