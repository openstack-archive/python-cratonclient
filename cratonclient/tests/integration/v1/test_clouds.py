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
"""The integration tests for the cratonclient.v1.clouds."""

from cratonclient.tests.integration import base


class TestClouds(base.BetamaxTestCase):
    """CloudsManager integration tests."""

    def setUp(self):
        """Prepare our clouds manager test case."""
        super(TestClouds, self).setUp()
        self.create_demo_client()

    def test_create(self):
        """Test cloud creation via the API."""
        note = 'This is a test cloud.'
        cloud = self.cleanupCloud(self.client.clouds.create(
            name='cloud-creation',
            note=note,
            variables={'cloud-var': 'var-value'},
        ))

        self.assertEqual('cloud-creation', cloud.name)
        self.assertEqual(note, cloud.note)
        self.assertEqual({'cloud-var': 'var-value'},
                         cloud.to_dict()['variables'])

    def test_delete(self):
        """Verify the client can delete a cloud."""
        cloud = self.client.clouds.create(name='cloud-deletion')

        self.assertEqual('cloud-deletion', cloud.name)

        self.assertTrue(self.client.clouds.delete(cloud.id))
        self.assertNotFound(self.client.clouds.get, cloud.id)

    def test_autopagination_when_listing(self):
        """Verify the client autopaginates lists of clouds."""
        note_str = 'This cloud was created to test pagination. ({}/62)'
        for i in range(0, 62):
            self.cleanupCloud(self.client.clouds.create(
                name='cloud-{}'.format(i),
                note=note_str.format(i),
            ))

        cells = list(self.client.clouds.list())
        self.assertEqual(62, len(cells))

    def test_manual_pagination(self):
        """Verify manual pagination of /v1/clouds."""
        note_str = 'This cloud was created to test pagination. ({}/62)'
        for i in range(0, 62):
            self.cleanupCloud(self.client.clouds.create(
                name='cloud-{}'.format(i),
                note=note_str.format(i),
            ))

        first_page = list(self.client.clouds.list(autopaginate=False))
        self.assertEqual(30, len(first_page))

        next_page = list(self.client.clouds.list(
            autopaginate=False,
            marker=first_page[-1].id,
        ))
        self.assertEqual(30, len(next_page))

        last_page = list(self.client.clouds.list(
            autopaginate=False,
            marker=next_page[-1].id,
        ))
        self.assertEqual(2, len(last_page))

    def test_update_existing_cloud(self):
        """Test that the client allows a cloud to be deleted."""
        cloud = self.cleanupCloud(self.client.clouds.create(
            name='cloud-to-update',
            note='Original note.',
        ))

        self.assertEqual('cloud-to-update', cloud.name)
        self.assertEqual('Original note.', cloud.note)

        updated_cloud = self.client.clouds.update(
            cloud.id,
            name='updated-cloud',
            note='Updated note.',
        )
        self.assertEqual(cloud.id, updated_cloud.id)
        self.assertEqual('updated-cloud', updated_cloud.name)
        self.assertEqual('Updated note.', updated_cloud.note)
