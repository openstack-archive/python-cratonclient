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
"""The integration tests for the cratonclient.v1.devices."""

from cratonclient.tests.integration import base


class TestDevices(base.BetamaxTestCase):
    """DevicesManager integration tests."""

    def cleanupCloud(self, cloud):
        """Add a cleanup task for this cloud."""
        self.addCleanup(self.client.clouds.delete, cloud.id)
        return cloud

    def cleanupRegion(self, region):
        """Add a cleanup task for this region."""
        self.addCleanup(self.client.regions.delete, region.id)
        return region

    def cleanupCell(self, cell):
        """Add a cleanup task for this cell."""
        self.addCleanup(self.client.cells.delete, cell.id)
        return cell

    def cleanupHost(self, host):
        """Add a cleanup task for this host."""
        self.addCleanup(self.client.hosts.delete, host.id)
        return host

    def setUp(self):
        """Set up our demo user client."""
        super(TestDevices, self).setUp()
        self.create_demo_client()
        test_name = self.cassette_name.split('-', 1)[-1]
        self.cloud = self.cleanupCloud(self.client.clouds.create(
            name='cloud_{}'.format(test_name),
        ))
        self.region = self.cleanupRegion(self.client.regions.create(
            name='region_{}'.format(test_name),
            cloud_id=self.cloud.id,
        ))
        self.cells = [
            self.cleanupCell(self.client.cells.create(
                name='cell_{}_{}'.format(test_name, i),
                region_id=self.region.id,
                cloud_id=self.cloud.id,
            ))
            for i in range(4)
        ]
        self.hosts = [
            self.cleanupHost(self.client.hosts.create(
                name='host_{}_{}'.format(test_name, i),
                cell_id=self.cells[i % 4].id,
                region_id=self.region.id,
                cloud_id=self.cloud.id,
                device_type='server',
                ip_address='127.0.1.{}'.format(i),
            ))
            for i in range(35)
        ]
        # NOTE(sigmavirus24): The API does not presently support
        # /v1/network-devices
        # self.network_devices = [
        #     self.cleanupNetworkDevice(self.client.network_devices.create(
        #     ))
        #     for i in range(35)
        # ]
