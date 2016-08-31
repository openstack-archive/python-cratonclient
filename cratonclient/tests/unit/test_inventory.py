#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""Tests for `cratonclient.v1.inventory` module."""

import mock

from cratonclient.tests import base
from cratonclient.v1 import inventory


class TestInventory(base.TestCase):
    """Test our craton inventory api class."""

    @mock.patch('cratonclient.v1.hosts.HostManager')
    def test_inventory_creates_host_manager(self, mock_hostmanager):
        """Verify Inventory class creates HostManager."""
        session = mock.Mock()
        url = 'https://10.1.1.0:8080/'
        region_id = 1,
        inventory.Inventory(session, url, region_id)
        mock_hostmanager.assert_called_once_with(session, url)
