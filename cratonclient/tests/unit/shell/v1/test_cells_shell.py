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
import mock

from cratonclient import exceptions
from cratonclient.shell.v1 import cells_shell
from cratonclient.tests.unit.shell import base
from cratonclient.v1 import cells


class TestDoShellShow(base.TestShellCommandUsingPrintDict):
    """Unit tests for the cell show command."""

    def test_simple_usage(self):
        """Verify the behaviour of do_cell_show."""
        args = self.args_for(
            region=123,
            id=456,
        )

        cells_shell.do_cell_show(self.craton_client, args)

        self.craton_client.cells.get.assert_called_once_with(456)
        self.print_dict.assert_called_once_with(
            {f: mock.ANY for f in cells.CELL_FIELDS},
            wrap=72,
        )


class TestDoCellList(base.TestShellCommandUsingPrintList):
    """Unit tests for the cell list command."""

    def assertNothingWasCalled(self):
        """Assert inventory, list, and print_list were not called."""
        super(TestDoCellList, self).assertNothingWasCalled()
        self.assertFalse(self.print_list.called)

    def args_for(self, **kwargs):
        """Generate the default argument list for cell-list."""
        kwargs.setdefault('region', 123)
        kwargs.setdefault('detail', False)
        kwargs.setdefault('limit', None)
        kwargs.setdefault('sort_key', None)
        kwargs.setdefault('sort_dir', 'asc')
        kwargs.setdefault('fields', [])
        kwargs.setdefault('marker', None)
        kwargs.setdefault('all', False)
        return super(TestDoCellList, self).args_for(**kwargs)

    def test_with_defaults(self):
        """Verify the behaviour of do_cell_list with mostly default values."""
        args = self.args_for()

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            sort_dir='asc',
            region_id=123,
            autopaginate=False,
            marker=None,
        )
        self.assertTrue(self.print_list.called)
        self.assertEqual(['id', 'name'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_negative_limit(self):
        """Ensure we raise an exception for negative limits."""
        args = self.args_for(limit=-1)

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_positive_limit(self):
        """Verify that we pass positive limits to the call to list."""
        args = self.args_for(limit=5)

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            limit=5,
            sort_dir='asc',
            region_id=123,
            autopaginate=False,
            marker=None,
        )
        self.assertTrue(self.print_list.called)
        self.assertEqual(['id', 'name'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_valid_sort_key(self):
        """Verify that we pass on our sort key."""
        args = self.args_for(sort_key='name')

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            sort_dir='asc',
            sort_key='name',
            region_id=123,
            autopaginate=False,
            marker=None,
        )
        self.assertTrue(self.print_list.called)
        self.assertEqual(['id', 'name'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_invalid_sort_key(self):
        """Verify that do not we pass on our sort key."""
        args = self.args_for(sort_key='fake-sort-key')

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_detail(self):
        """Verify the behaviour of specifying --detail."""
        args = self.args_for(detail=True)

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            sort_dir='asc',
            detail=True,
            region_id=123,
            autopaginate=False,
            marker=None,
        )
        self.assertEqual(sorted(list(cells.CELL_FIELDS)),
                         sorted(self.print_list.call_args[0][-1]))

    def test_raises_exception_with_detail_and_fields(self):
        """Verify that we fail when users specify --detail and --fields."""
        args = self.args_for(
            detail=True,
            fields=['id', 'name'],
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_fields(self):
        """Verify that we print out specific fields."""
        args = self.args_for(fields=['id', 'name', 'note'])

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            sort_dir='asc',
            region_id=123,
            autopaginate=False,
            marker=None,
        )
        self.assertEqual(['id', 'name', 'note'],
                         sorted(self.print_list.call_args[0][-1]))

    def test_invalid_fields(self):
        """Verify that we error out with invalid fields."""
        args = self.args_for(fields=['uuid', 'not-name', 'nate'])

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_list, args)
        self.assertNothingWasCalled()

    def test_autopaginate(self):
        """Verify that autopagination works."""
        args = self.args_for(all=True)

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            sort_dir='asc',
            region_id=123,
            limit=100,
            autopaginate=True,
            marker=None,
        )

    def test_autopagination_overrides_limit(self):
        """Verify that --all overrides --limit."""
        args = self.args_for(all=True, limit=10)

        cells_shell.do_cell_list(self.craton_client, args)

        self.craton_client.cells.list.assert_called_once_with(
            sort_dir='asc',
            region_id=123,
            limit=100,
            autopaginate=True,
            marker=None,
        )


class TestDoCellCreate(base.TestShellCommandUsingPrintDict):
    """Unit tests for the cell create command."""

    def args_for(self, **kwargs):
        """Generate the default args for cell-create."""
        kwargs.setdefault('name', 'New Cell')
        kwargs.setdefault('region_id', 123)
        kwargs.setdefault('note', None)
        return super(TestDoCellCreate, self).args_for(**kwargs)

    def test_create_without_note(self):
        """Verify our parameters to cells.create."""
        args = self.args_for()

        cells_shell.do_cell_create(self.craton_client, args)

        self.craton_client.cells.create.assert_called_once_with(
            name='New Cell',
            region_id=123,
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_create_with_note(self):
        """Verify that we include the note argument when present."""
        args = self.args_for(note='This is a note')

        cells_shell.do_cell_create(self.craton_client, args)

        self.craton_client.cells.create.assert_called_once_with(
            name='New Cell',
            region_id=123,
            note='This is a note',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)


class TestDoCellUpdate(base.TestShellCommandUsingPrintDict):
    """Unit tests for the cell update command."""

    def args_for(self, **kwargs):
        """Generate arguments for cell-update command."""
        kwargs.setdefault('id', 123)
        kwargs.setdefault('name', None)
        kwargs.setdefault('region_id', None)
        kwargs.setdefault('note', None)
        return super(TestDoCellUpdate, self).args_for(**kwargs)

    def test_update_without_name_region_or_note_fails(self):
        """Verify we raise a command error when there's nothing to update."""
        args = self.args_for()

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_update, args)
        self.assertNothingWasCalled()

    def test_update_with_name(self):
        """Verify we update with only the new name."""
        args = self.args_for(name='New name')

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.cells.update.assert_called_once_with(
            123,
            name='New name',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_update_with_new_region(self):
        """Verify we update with only the new region id."""
        args = self.args_for(region_id=678)

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.cells.update.assert_called_once_with(
            123,
            region_id=678,
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_update_with_new_note(self):
        """Verify we update with only the new note text."""
        args = self.args_for(note='A new note')

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.cells.update.assert_called_once_with(
            123,
            note='A new note',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)

    def test_update_with_everything(self):
        """Verify we update with everything."""
        args = self.args_for(
            name='A new name for a new region',
            region_id=678,
            note='A new note',
        )

        cells_shell.do_cell_update(self.craton_client, args)

        self.craton_client.cells.update.assert_called_once_with(
            123,
            name='A new name for a new region',
            region_id=678,
            note='A new note',
        )
        self.print_dict.assert_called_once_with(mock.ANY, wrap=72)


class TestDoCellDelete(base.TestShellCommand):
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
        self.craton_client.cells.delete.return_value = True
        args = self.args_for(
            id=456,
        )

        cells_shell.do_cell_delete(self.craton_client, args)

        self.craton_client.cells.delete.assert_called_once_with(456)
        self.print_func.assert_called_once_with(
            'Cell 456 was successfully deleted.'
        )

    def test_failed(self):
        """Verify the message we print when deletion fails."""
        self.craton_client.cells.delete.return_value = False
        args = self.args_for(
            id=456,
        )

        cells_shell.do_cell_delete(self.craton_client, args)

        self.craton_client.cells.delete.assert_called_once_with(456)
        self.print_func.assert_called_once_with(
            'Cell 456 was not deleted.'
        )

    def test_failed_with_exception(self):
        """Verify the message we print when deletion fails."""
        self.craton_client.cells.delete.side_effect = exceptions.NotFound
        args = self.args_for(
            region=123,
            id=456,
        )

        self.assertRaisesCommandErrorWith(cells_shell.do_cell_delete, args)

        self.craton_client.cells.delete.assert_called_once_with(456)
        self.assertFalse(self.print_func.called)
