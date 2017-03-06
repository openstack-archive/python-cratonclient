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
"""Module containing the cratonclient.v1.hosts integration tests."""

from cratonclient.tests.integration import base


class TestHosts(base.BetamaxTestCase):
    """HostsManager integration tests."""

    def test_create(self):
        """Test creation of hosts via the Python API."""
        self.create_demo_client()

        cloud = self.client.clouds.create(name='cloud-0')
        region = self.client.regions.create(name='region-0')
        host = self.client.hosts.create(
            name='host-0',
            ip_address='127.0.1.0',
            type='server',
            region_id=region.id,
            cloud_id=cloud.id,
        )

        self.assertEqual('host-0', host.name)
