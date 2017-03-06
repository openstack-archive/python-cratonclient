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

    def setUp(self):
        super(TestHosts, self).setUp()
        self.create_demo_client()

    def test_create(self):
        """Test creation of hosts via the Python API."""
        cloud = self.client.clouds.create(name='cloud-0')
        region = self.client.regions.create(
            name='region-0',
            cloud_id=cloud.id,
        )
        host = self.client.hosts.create(
            name='host-0',
            ip_address='127.0.1.0',
            device_type='server',
            region_id=region.id,
            cloud_id=cloud.id,
        )

        self.assertEqual('host-0', host.name)

    def test_list_autopaginates(self):
        """Verify listing of hosts via the Python API."""
        # NOTE(sigmavirus24): This relies on the API being populated with 61
        # hosts, e.g.,
        cloud = self.client.clouds.create(name='cloud-0')
        region = self.client.regions.create(
            name='region-0',
            cloud_id=cloud.id,
        )
        for i in range(0, 62):
            self.client.hosts.create(
                name='host-{}'.format(i),
                ip_address='127.0.1.{}'.format(i),
                device_type='server',
                region_id=region.id,
                cloud_id=cloud.id,
            )

        hosts = list(self.client.hosts.list())
        self.assertEqual(61, hosts)

#    def test_list_only_retrieves_first_page(self):
#        """Verify the behaviour of not auto-paginating listing."""
#        for i in range(0, 32):
#            self.client.hosts.create(
#                name='host-{}'.format(i),
#                ip_address='127.0.1.{}'.format(i),
#                device_type='server',
#                region_id=self.region.id,
#                cloud_id=self.cloud.id,
#            )
#
#        hosts = list(self.client.hosts.list(autopaginate=False))
#        self.assertEqual(30, hosts)
