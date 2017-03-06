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

from cratonclient import exceptions
from cratonclient.tests.integration import base


class TestHosts(base.BetamaxTestCase):
    """HostsManager integration tests."""

    def setUp(self):
        """Prepare our hosts test case."""
        super(TestHosts, self).setUp()
        self.create_demo_client()
        self.cloud = self.client.clouds.create(name='cloud-0')
        self.region = self.client.regions.create(
            name='region-0',
            cloud_id=self.cloud.id,
        )

    def test_create(self):
        """Test creation of hosts via the Python API."""
        host = self.client.hosts.create(
            name='host-0',
            ip_address='127.0.1.0',
            device_type='server',
            region_id=self.region.id,
            cloud_id=self.cloud.id,
        )

        self.assertEqual('host-0', host.name)

    def test_delete(self):
        """Test deletion of a host via the Python API."""
        host = self.client.hosts.create(
            name='host-to-delete',
            ip_address='127.0.1.0',
            device_type='server',
            region_id=self.region.id,
            cloud_id=self.cloud.id,
        )

        self.assertTrue(self.client.hosts.delete(host.id))
        self.assertRaises(exceptions.NotFound, self.client.hosts.get,
                          host.id)

    def test_list_autopaginates(self):
        """Verify listing of hosts via the Python API."""
        for i in range(0, 62):
            self.client.hosts.create(
                name='host-{}'.format(i),
                ip_address='127.0.1.{}'.format(i),
                device_type='server',
                region_id=self.region.id,
                cloud_id=self.cloud.id,
            )

        hosts = list(self.client.hosts.list())
        self.assertEqual(62, len(hosts))

    def test_list_only_retrieves_first_page(self):
        """Verify the behaviour of not auto-paginating listing."""
        for i in range(0, 32):
            self.client.hosts.create(
                name='host-{}'.format(i),
                ip_address='127.0.1.{}'.format(i),
                device_type='server',
                region_id=self.region.id,
                cloud_id=self.cloud.id,
            )

        hosts = list(self.client.hosts.list(autopaginate=False))
        self.assertEqual(30, len(hosts))

    def test_update(self):
        """Verify the ability to update a host."""
        host = self.client.hosts.create(
            name='host-0',
            ip_address='127.0.1.0',
            device_type='server',
            region_id=self.region.id,
            cloud_id=self.cloud.id,
        )

        self.assertTrue(host.active)

        updated_host = self.client.hosts.update(
            item_id=host.id,
            note='This is an updated note',
            ip_address='127.0.1.1',
        )

        self.assertEqual('host-0', updated_host.name)
        self.assertEqual(host.id, updated_host.id)
        self.assertEqual('This is an updated note', updated_host.note)
