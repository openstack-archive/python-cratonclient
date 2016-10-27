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
"""Tests for `cratonclient.v1.regions` module."""

from cratonclient import crud
from cratonclient.tests import base
from cratonclient.v1 import regions

import mock


class TestRegion(base.TestCase):
    """Tests for the Region Resource."""

    def test_is_a_resource_instance(self):
        """Verify that a Region instance is an instance of a Resource."""
        manager = mock.Mock()
        self.assertIsInstance(regions.Region(manager, {}),
                              crud.Resource)


class TestRegionManager(base.TestCase):
    """Tests for the RegionManager class."""

    def test_is_a_crudclient(self):
        """Verify our RegionManager is a CRUDClient."""
        session = mock.Mock()
        region_mgr = regions.RegionManager(session, '')
        self.assertIsInstance(region_mgr, crud.CRUDClient)
