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

"""Tests for `cratonclient.shell.v1.cells_shell` module."""

import mock
import re

from argparse import Namespace
from testtools import matchers

from cratonclient import exceptions as exc
from cratonclient.shell.v1 import cells_shell
from cratonclient.tests.integration import base
from cratonclient.v1 import cells


class TestCellsShell(base.ShellTestCase):
    """Test our craton cells shell commands."""

    re_options = re.DOTALL | re.MULTILINE
    cell_valid_fields = None
    cell_invalid_field = None

    def setUp(self):
        """Setup required test fixtures."""
        super(TestCellsShell, self).setUp()
        self.cell_valid_fields = Namespace(project_id=1,
                                           region_id=1,
                                           name='mock_cell')
        self.cell_invalid_field = Namespace(project_id=1,
                                            region_id=1,
                                            name='mock_cell',
                                            invalid_foo='ignored')

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_success(self, mock_list):
        """Verify that no arguments prints out all project cells."""
        self.shell('cell-list -r 1')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_parse_param_success(self, mock_list):
        """Verify that success of parsing a subcommand argument."""
        self.shell('cell-list -r 1 --limit 0')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_limit_0_success(self, mock_list):
        """Verify that --limit 0 prints out all project cells."""
        self.shell('cell-list -r 1 --limit 0')
        mock_list.assert_called_once_with(
            limit=0,
            region_id=1,
        )

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_limit_positive_num_success(self, mock_list):
        """Verify --limit X, where X is a positive integer, succeeds.

        The command will print out X number of project cells.
        """
        self.shell('cell-list -r 1 --limit 1')
        mock_list.assert_called_once_with(
            limit=1,
            region_id=1,
        )

    def test_cell_list_limit_negative_num_failure(self):
        """Verify --limit X, where X is a negative integer, fails.

        The command will cause a Command Error message response.
        """
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'cell-list -r 1 --limit -1')

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_detail_success(self, mock_list):
        """Verify --detail argument successfully pass detail to Client."""
        self.shell('cell-list -r 1 --detail')
        mock_list.assert_called_once_with(
            detail=True,
            region_id=1,
        )

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    @mock.patch('cratonclient.common.cliutils.print_list')
    def test_cell_list_fields_success(self, mock_printlist, mock_list):
        """Verify --fields argument successfully passed to Client."""
        self.shell('cell-list -r 1 --fields id name')
        mock_list.assert_called_once_with(
            region_id=1,
        )
        mock_printlist.assert_called_once_with(mock.ANY,
                                               list({'id': 'ID',
                                                     'name': 'Name'}))

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_sort_key_field_key_success(self, mock_list):
        """Verify --sort-key arguments successfully passed to Client."""
        self.shell('cell-list -r 1 --sort-key name')
        mock_list.assert_called_once_with(
            sort_key='name',
            region_id=1,
        )

    def test_cell_list_sort_key_invalid(self):
        """Verify --sort-key with invalid args, fails with Command Error."""
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'cell-list -r 1 --sort-key invalid')

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_sort_dir_asc_success(self, mock_list):
        """Verify --sort-dir asc successfully passed to Client."""
        self.shell('cell-list -r 1 --sort-key name --sort-dir asc')
        mock_list.assert_called_once_with(
            sort_key='name',
            sort_dir='asc',
            region_id=1,
        )

    @mock.patch('cratonclient.v1.cells.CellManager.list')
    def test_cell_list_sort_dir_desc_success(self, mock_list):
        """Verify --sort-dir desc successfully passed to Client."""
        self.shell('cell-list -r 1 --sort-key name --sort-dir desc')
        mock_list.assert_called_once_with(
            sort_key='name',
            sort_dir='desc',
            region_id=1,
        )

    def test_cell_list_sort_dir_invalid_value(self):
        """Verify --sort-dir with invalid args, fails with Command Error."""
        (_, error) = self.shell(
            'cell-list -r 1 --sort-key name --sort-dir invalid'
        )
        self.assertIn("invalid choice: 'invalid'", error)

    def test_cell_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cell-create',
            '.*?^craton cell-create: error:.*$'
        ]
        stdout, stderr = self.shell('cell-create')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.cells.CellManager.create')
    def test_do_cell_create_calls_cell_manager_with_fields(self, mock_create):
        """Verify that do cell create calls CellManager create."""
        client = mock.Mock()
        client.cells = cells.CellManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        cells_shell.do_cell_create(client, self.cell_valid_fields)
        mock_create.assert_called_once_with(**vars(self.cell_valid_fields))

    @mock.patch('cratonclient.v1.cells.CellManager.create')
    def test_do_cell_create_ignores_unknown_fields(self, mock_create):
        """Verify that do cell create ignores unknown field."""
        client = mock.Mock()
        client.cells = cells.CellManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        cells_shell.do_cell_create(client, self.cell_invalid_field)
        mock_create.assert_called_once_with(**vars(self.cell_valid_fields))

    def test_cell_update_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cell-update',
            '.*?^craton cell-update: error:.*$',
        ]
        stdout, stderr = self.shell('cell-update')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.cells.CellManager.update')
    def test_do_cell_update_calls_cell_manager_with_fields(self, mock_update):
        """Verify that do cell update calls CellManager update."""
        client = mock.Mock()
        client.cells = cells.CellManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        valid_input = Namespace(region=1,
                                id=1,
                                name='mock_cell')
        cells_shell.do_cell_update(client, valid_input)
        mock_update.assert_called_once_with(1, name='mock_cell')

    @mock.patch('cratonclient.v1.cells.CellManager.update')
    def test_do_cell_update_ignores_unknown_fields(self, mock_update):
        """Verify that do cell update ignores unknown field."""
        client = mock.Mock()
        client.cells = cells.CellManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        invalid_input = Namespace(region=1,
                                  id=1,
                                  name='mock_cell',
                                  invalid=True)
        cells_shell.do_cell_update(client, invalid_input)
        mock_update.assert_called_once_with(1, name='mock_cell')

    def test_cell_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cell-show',
            '.*?^craton cell-show: error:.*$',
        ]
        stdout, stderr = self.shell('cell-show')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.cells.CellManager.get')
    def test_do_cell_show_calls_cell_manager_with_fields(self, mock_get):
        """Verify that do cell show calls CellManager get."""
        client = mock.Mock()
        client.cells = cells.CellManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        test_args = Namespace(id=1)
        cells_shell.do_cell_show(client, test_args)
        mock_get.assert_called_once_with(vars(test_args)['id'])

    def test_cell_delete_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cell-delete',
            '.*?^craton cell-delete: error:.*$',
        ]
        stdout, stderr = self.shell('cell-delete')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.cells.CellManager.delete')
    def test_do_cell_delete_calls_cell_manager_with_fields(self, mock_delete):
        """Verify that do cell delete calls CellManager delete."""
        client = mock.Mock()
        client.cells = cells.CellManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        test_args = Namespace(id=1, region=1)
        cells_shell.do_cell_delete(client, test_args)
        mock_delete.assert_called_once_with(vars(test_args)['id'])
