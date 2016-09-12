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
"""Tests for `cratonclient` module."""
import mock

from cratonclient.tests import base
from cratonclient.v1 import client


class TestCratonclient(base.TestCase):
    """Tests for the top-level module."""

    def test_something(self):
        """Do nothing."""
        pass

    @mock.patch('cratonclient.v1.inventory.Inventory')
    def test_client_creates_inventory(self, mock_inventory):
        """Verify that Craton client creates Inventory."""
        session = mock.Mock()
        url = 'https://10.1.1.8080'
        region_id = 1
        craton = client.Client(session, url)
        craton.inventory(region_id)
        mock_inventory.assert_called_once_with(region_id=region_id,
                                               session=session,
                                               url=url + '/v1')
