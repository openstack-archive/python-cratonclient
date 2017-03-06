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
"""Tests for `cratonclient.v1.clouds` module."""

from cratonclient import crud
from cratonclient.tests import base
from cratonclient.v1 import clouds

import mock


class TestCloud(base.TestCase):
    """Tests for the Cloud Resource."""

    def test_is_a_resource_instance(self):
        """Verify that a Cloud instance is an instance of a Resource."""
        manager = mock.Mock()
        manager.extra_request_kwargs = {}
        self.assertIsInstance(clouds.Cloud(manager, {"id": 1234}),
                              crud.Resource)


class TestCloudManager(base.TestCase):
    """Tests for the CloudManager class."""

    def test_is_a_crudclient(self):
        """Verify our CloudManager is a CRUDClient."""
        session = mock.Mock()
        cloud_mgr = clouds.CloudManager(session, '')
        self.assertIsInstance(cloud_mgr, crud.CRUDClient)
