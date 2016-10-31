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
"""Tests for the shell functions for the cells resource."""
import argparse

import mock

from cratonclient import exceptions
from cratonclient.shell.v1 import cells_shell
from cratonclient.tests import base
from cratonclient.v1 import cells


class TestCells(base.TestCase):
    """Base class for cells_shell commands."""

    def setUp(self):
        """Initialize test fixtures."""
        super(TestCells, self).setUp()
        self.craton_client = mock.Mock()
        self.inventory = mock.Mock()
        self.craton_client.inventory.return_value = self.inventory

    def assertRaisesCommandErrorWith(self, func, args):
        """Assert do_cell_create raises CommandError."""
        self.assertRaises(
            exceptions.CommandError,
            func, self.craton_client, args,
        )


class TestCellsPrintDict(TestCells):
    """Base class for commands using print_dict."""

    def setUp(self):
        """Initialize test fixtures."""
        super(TestCellsPrintDict, self).setUp()
        self.print_dict_patch = mock.patch(
            'cratonclient.common.cliutils.print_dict'
        )
        self.print_dict = self.print_dict_patch.start()

    def tearDown(self):
        """Clean-up test fixtures."""
        super(TestCellsPrintDict, self).tearDown()
        self.print_dict_patch.stop()

    def assertNothingWasCalled(self):
        """Assert inventory, list, and print_dict were not called."""
        self.assertFalse(self.craton_client.inventory.called)
        self.assertFalse(self.inventory.cells.list.called)
        self.assertFalse(self.print_dict.called)


class TestDoShellShow(TestCellsPrintDict):
    """Unit tests for the cell show command."""

    def test_simple_usage(self):
        """Verify the behaviour of do_cell_show."""
        args = argparse.Namespace(
            region=123,
            id=456,
        )

        cells_shell.do_cell_show(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.get.assert_called_once_with(456)
        self.print_dict.assert_called_once_with(
            {f: mock.ANY for f in cells.CELL_FIELDS},
            wrap=72,
        )


class TestDoCellList(TestCells):
    """Unit tests for the cell list command."""

    def setUp(self):
        """Initialize test fixtures."""
        super(TestDoCellList, self).setUp()
        self.print_list_patch = mock.patch(
            'cratonclient.common.cliutils.print_list'
        )
        self.print_list = self.print_list_patch.start()

    def tearDown(self):
        """Clean-up test fixtures."""
        super(TestDoCellList, self).tearDown()
        self.print_list_patch.stop()

    def assertNothingWasCalled(self):
        """Assert inventory, list, and print_list were not called."""
        self.assertFalse(self.craton_client.inventory.called)
        self.assertFalse(self.inventory.cells.list.called)
        self.assertFalse(self.print_list.called)

    def test_with_defaults(self):
        """Verify the behaviour of do_cell_list with mostly default values."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=None,
            sort_key=None,
            sort_dir='asc',
            fields=[],
        )

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.list.assert_called_once_with(sort_dir='asc')
        self.assertTrue(self.print_list.called)
        self.assertEqual(['id', 'name'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_negative_limit(self):
        """Ensure we raise an exception for negative limits."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=-1,
            sort_key=None,
            sort_dir='asc',
            fields=[],
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_positive_limit(self):
        """Verify that we pass positive limits to the call to list."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=5,
            sort_key=None,
            sort_dir='asc',
            fields=[],
        )

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.list.assert_called_once_with(
            limit=5,
            sort_dir='asc',
        )
        self.assertTrue(self.print_list.called)
        self.assertEqual(['id', 'name'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_valid_sort_key(self):
        """Verify that we pass on our sort key."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=None,
            sort_key='name',
            sort_dir='asc',
            fields=[],
        )

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.list.assert_called_once_with(
            sort_dir='asc',
            sort_key='name',
        )
        self.assertTrue(self.print_list.called)
        self.assertEqual(['id', 'name'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_invalid_sort_key(self):
        """Verify that do not we pass on our sort key."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=None,
            sort_key='fake-sort-key',
            sort_dir='asc',
            fields=[],
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_detail(self):
        """Verify the behaviour of specifying --detail."""
        args = argparse.Namespace(
            region=123,
            detail=True,
            limit=None,
            sort_key=None,
            sort_dir='asc',
            fields=[],
        )

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.list.assert_called_once_with(
            sort_dir='asc',
            detail=True,
        )
        self.assertEqual(sorted(list(cells.CELL_FIELDS)),
                         sorted(self.print_list.call_args[0][-1]))

    def test_raises_exception_with_detail_and_fields(self):
        """Verify that we fail when users specify --detail and --fields."""
        args = argparse.Namespace(
            region=123,
            detail=True,
            limit=None,
            sort_key=None,
            sort_dir='asc',
            fields=['id', 'name'],
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_fields(self):
        """Verify that we print out specific fields."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=None,
            sort_key=None,
            sort_dir='asc',
            fields=['id', 'name', 'note'],
        )

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.list.assert_called_once_with(
            sort_dir='asc',
        )
        self.assertEqual(['id', 'name', 'note'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_invalid_fields(self):
        """Verify that we error out with invalid fields."""
        args = argparse.Namespace(
            region=123,
            detail=False,
            limit=None,
            sort_key=None,
            sort_dir='asc',
            fields=['uuid', 'not-name', 'nate'],
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()


class TestDoCellCreate(TestCellsPrintDict):
    """Unit tests for the cell create command."""

    def test_create_without_note(self):
        """Verify our parameters to cells.create."""
        args = argparse.Namespace(
            name='New Cell',
            region_id=123,
            note=None,
        )

        cells_shell.do_cell_create(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.create.assert_called_once_with(
            name='New Cell',
            region_id=123,
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_create_with_note(self):
        """Verify that we include the note argument when present."""
        args = argparse.Namespace(
            name='New Cell',
            region_id=123,
            note='This is a note',
        )

        cells_shell.do_cell_create(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.create.assert_called_once_with(
            name='New Cell',
            region_id=123,
            note='This is a note',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)


class TestDoCellUpdate(TestCellsPrintDict):
    """Unit tests for the cell update command."""

    def test_update_without_name_region_or_note_fails(self):
        """Verify we raise a command error when there's nothing to update."""
        args = argparse.Namespace(
            id=123,
            region=345,
            name=None,
            region_id=None,
            note=None,
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_update, args)
        self.assertNothingWasCalled()

    def test_update_with_name(self):
        """Verify we update with only the new name."""
        args = argparse.Namespace(
            id=123,
            region=345,
            name='New name',
            region_id=None,
            note=None,
        )

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(345)
        self.inventory.cells.update.assert_called_once_with(
            123,
            name='New name',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_update_with_new_region(self):
        """Verify we update with only the new region id."""
        args = argparse.Namespace(
            id=123,
            region=345,
            name=None,
            region_id=678,
            note=None,
        )

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(345)
        self.inventory.cells.update.assert_called_once_with(
            123,
            region_id=678,
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_update_with_new_note(self):
        """Verify we update with only the new note text."""
        args = argparse.Namespace(
            id=123,
            region=345,
            name=None,
            region_id=None,
            note='A new note',
        )

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(345)
        self.inventory.cells.update.assert_called_once_with(
            123,
            note='A new note',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_update_with_everything(self):
        """Verify we update with everything."""
        args = argparse.Namespace(
            id=123,
            region=345,
            name='A new name for a new region',
            region_id=678,
            note='A new note',
        )

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(345)
        self.inventory.cells.update.assert_called_once_with(
            123,
            name='A new name for a new region',
            region_id=678,
            note='A new note',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)


class TestDoCellDelete(TestCells):
    """Tests for the do_cell_delete command."""

    def setUp(self):
        """Initialize our print mock."""
        super(TestDoCellDelete, self).setUp()
        self.print_func_mock = mock.patch(
            'cratonclient.shell.v1.cells_shell.print'
        )
        self.print_func = self.print_func_mock.start()

    def tearDown(self):
        """Clean up our print mock."""
        super(TestDoCellDelete, self).tearDown()
        self.print_func_mock.stop()

    def test_successful(self):
        """Verify the message we print when successful."""
        self.inventory.cells.delete.return_value = True
        args = argparse.Namespace(
            region=123,
            id=456,
        )

        cells_shell.do_cell_delete(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.delete.assert_called_once_with(456)
        self.print_func.assert_called_once_with(
            'Cell 456 was successfully deleted.'
        )

    def test_failed(self):
        """Verify the message we print when deletion fails."""
        self.inventory.cells.delete.return_value = False
        args = argparse.Namespace(
            region=123,
            id=456,
        )

        cells_shell.do_cell_delete(self.craton_client, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.delete.assert_called_once_with(456)
        self.print_func.assert_called_once_with(
            'Cell 456 was not deleted.'
        )

    def test_failed_with_exception(self):
        """Verify the message we print when deletion fails."""
        self.inventory.cells.delete.side_effect = exceptions.NotFound
        args = argparse.Namespace(
            region=123,
            id=456,
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_delete, args)

        self.craton_client.inventory.assert_called_once_with(123)
        self.inventory.cells.delete.assert_called_once_with(456)
        self.assertFalse(self.print_func.called)
