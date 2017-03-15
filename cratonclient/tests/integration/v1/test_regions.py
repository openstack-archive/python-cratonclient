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
"""Module containing the cratonclient.v1.regions integration tests."""

from cratonclient.tests.integration import base


class TestRegions(base.BetamaxTestCase):
    """Tests for v1 RegionsManager."""

    def cleanupCloud(self, cloud):
        """Add a cleanup task for this cloud."""
        self.addCleanup(self.client.clouds.delete, cloud.id)
        return cloud

    def cleanupRegion(self, region):
        """Add a cleanup task for this region."""
        self.addCleanup(self.client.regions.delete, region.id)
        return region

    def setUp(self):
        """Prepare our test case for regions."""
        super(TestRegions, self).setUp()
        self.create_demo_client()
        self.cloud = self.cleanupCloud(self.client.clouds.create(
            name='cloud-0',
        ))

    def test_create(self):
        """Verify creation of regions via the API."""
        region = self.cleanupRegion(self.client.regions.create(
            name='region-creation',
            cloud_id=self.cloud.id,
        ))

        self.assertEqual('region-creation', region.name)
        self.assertEqual(self.cloud.id, region.cloud_id)

        same_region = self.client.regions.get(region.id)
        self.assertEqual(region.id, same_region.id)
        self.assertEqual(region.name, same_region.name)
        self.assertEqual(region.cloud_id, same_region.cloud_id)

    def test_delete(self):
        """Verify deletion of regions via the API."""
        region = self.client.regions.create(
            name='region-creation',
            cloud_id=self.cloud.id,
        )

        self.assertTrue(self.client.regions.delete(region.id))
        self.assertNotFound(self.client.regions.get, region.id)

    def test_list_autopaginates(self):
        """Verify autopagination when listing regions."""
        for i in range(64):
            self.cleanupRegion(self.client.regions.create(
                name='regions-autopaginate-{}'.format(i),
                cloud_id=self.cloud.id,
            ))

        regions = list(self.client.regions.list())
        self.assertEqual(64, len(regions))

    def test_manual_pagination(self):
        """Verify manual pagination of regions."""
        for i in range(64):
            self.cleanupRegion(self.client.regions.create(
                name='regions-manual-list-{}'.format(i),
                cloud_id=self.cloud.id,
            ))

        first_page = list(self.client.regions.list(autopaginate=False))
        self.assertEqual(30, len(first_page))
        next_page = list(self.client.regions.list(
            autopaginate=False,
            marker=first_page[-1].id,
        ))
        self.assertEqual(30, len(next_page))
        last_page = list(self.client.regions.list(
            autopaginate=False,
            marker=next_page[-1].id,
        ))
        self.assertEqual(4, len(last_page))

    def test_update(self):
        """Verify the ability to update a given region."""
        region = self.cleanupRegion(self.client.regions.create(
            name='region-to-update',
            cloud_id=self.cloud.id,
        ))

        self.assertTrue('region-to-update', region.name)
        self.assertIsNone(region.note)

        updated_region = self.client.regions.update(
            region.id,
            name='region_updated',
            note='Here I add my note.',
        )

        self.assertEqual(region.id, updated_region.id)
        self.assertNotEqual(region.name, updated_region.name)
        self.assertEqual('region_updated', updated_region.name)
        self.assertEqual('Here I add my note.', updated_region.note)
