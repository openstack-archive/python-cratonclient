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
"""Module containing the cratonclient.v1.cells integration tests."""

from cratonclient.tests.integration import base


class TestCells(base.BetamaxTestCase):
    """CellsManager integration tests."""

    def setUp(self):
        """Prepare our cells test case."""
        super(TestCells, self).setUp()
        self.create_demo_client()
        self.cloud = self.client.clouds.create(name='cells-cloud-0')
        self.region = self.client.regions.create(
            name='cells-region-0',
            cloud_id=self.cloud.id,
        )

    def test_create(self):
        """Test creation of a cell via the API."""
        note = 'This is a test cell. There are many like it, but this is mine'
        cell = self.client.cells.create(
            name='cell-0',
            region_id=self.region.id,
            cloud_id=self.cloud.id,
            note=note,
            variables={'a': 'b'},
        )

        self.assertEqual('cell-0', cell.name)
        self.assertEqual(self.region.id, cell.region_id)
        self.assertEqual(self.cloud.id, cell.cloud_id)
        self.assertEqual(note, cell.note)

    def test_delete(self):
        """Test deleting a cell after creating it."""
        cell = self.client.cells.create(
            name='cell-to-delete',
            region_id=self.region.id,
            cloud_id=self.cloud.id,
        )

        self.assertEqual('cell-to-delete', cell.name)
        self.assertTrue(self.client.cells.delete(cell.id))
        self.assertNotFound(self.client.cells.get, cell.id)

    def test_autopagination_when_listing(self):
        """Verify the client autopaginates lists of cells."""
        note_str = 'This was created automatically for pagination. ({}/63)'
        for i in range(0, 63):
            self.client.cells.create(
                name='pagination-cell-{}'.format(i),
                region_id=self.region.id,
                cloud_id=self.cloud.id,
                note=note_str.format(i),
            )

        cells = list(self.client.cells.list())
        self.assertEqual(63, len(cells))

    def test_manual_pagination(self):
        """Verify manual pagination of cells."""
        note_str = 'This was created automatically for pagination. ({}/63)'
        for i in range(0, 63):
            self.client.cells.create(
                name='pagination-cell-{}'.format(i),
                region_id=self.region.id,
                cloud_id=self.cloud.id,
                note=note_str.format(i),
            )

        cells = list(self.client.cells.list(autopaginate=False))
        self.assertEqual(30, len(cells))

        next_page = list(self.client.cells.list(
            marker=cells[-1].id,
            autopaginate=False,
        ))
        self.assertEqual(30, len(next_page))

        last_page = list(self.client.cells.list(
            marker=next_page[-1].id,
            autopaginate=False,
        ))
        self.assertEqual(3, len(last_page))

    def test_update_existing_cell(self):
        """Verify we can update a cell."""
        cell = self.client.cells.create(
            name='cell-to-update',
            region_id=self.region.id,
            cloud_id=self.cloud.id,
            note='Original note',
            variables={'out-with': 'the-old'},
        )

        self.assertEqual('cell-to-update', cell.name)
        self.assertEqual('Original note', cell.note)

        updated_cell = self.client.cells.update(
            item_id=cell.id,
            note='Updated note.',
        )
        self.assertEqual(cell.id, updated_cell.id)
        self.assertEqual(cell.name, updated_cell.name)
        self.assertEqual('Updated note.', updated_cell.note)
