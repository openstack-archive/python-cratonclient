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

"""Tests for `cratonclient.shell.v1.hosts_shell` module."""

import mock
import re

from argparse import Namespace
from testtools import matchers

from cratonclient import exceptions as exc
from cratonclient.shell.v1 import hosts_shell
from cratonclient.tests.integration.shell import base
from cratonclient.v1 import hosts


class TestHostsShell(base.ShellTestCase):
    """Test our craton hosts shell commands."""

    re_options = re.DOTALL | re.MULTILINE
    host_valid_fields = None
    host_invalid_fields = None

    def setUp(self):
        """Setup required test fixtures."""
        super(TestHostsShell, self).setUp()
        self.host_valid_kwargs = {
            'project_id': 1,
            'region_id': 1,
            'name': 'mock_host',
            'ip_address': '127.0.0.1',
            'active': True,
        }
        self.host_invalid_kwargs = {
            'project_id': 1,
            'region_id': 1,
            'name': 'mock_host',
            'ip_address': '127.0.0.1',
            'active': True,
            'invalid_foo': 'ignored',
        }
        self.host_valid_fields = Namespace(**self.host_valid_kwargs)
        self.host_valid_fields.formatter = mock.Mock()
        self.host_invalid_fields = Namespace(**self.host_invalid_kwargs)
        self.host_invalid_fields.formatter = mock.Mock()

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_success(self, mock_list):
        """Verify that no arguments prints out all project hosts."""
        self.shell('host-list -r 1')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_parse_param_success(self, mock_list):
        """Verify that success of parsing a subcommand argument."""
        self.shell('host-list -r 1 --limit 0')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_limit_0_success(self, mock_list):
        """Verify that --limit 0 prints out all project hosts."""
        self.shell('host-list -r 1 --limit 0')
        mock_list.assert_called_once_with(
            limit=0,
            sort_dir='asc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_limit_positive_num_success(self, mock_list):
        """Verify --limit X, where X is a positive integer, succeeds.

        The command will print out X number of project hosts.
        """
        self.shell('host-list -r 1 --limit 1')
        mock_list.assert_called_once_with(
            limit=1,
            sort_dir='asc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    def test_host_list_limit_negative_num_failure(self):
        """Verify --limit X, where X is a negative integer, fails.

        The command will cause a Command Error message response.
        """
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'host-list -r 1 --limit -1')

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_cell_success(self, mock_list):
        """Verify --cell arguments successfully pass cell to Client."""
        for cell_arg in ['-c', '--cell']:
            self.shell('host-list -r 1 {0} 1'.format(cell_arg))
            mock_list.assert_called_once_with(
                cell_id=1,
                sort_dir='asc',
                region_id=1,
                marker=None,
                autopaginate=False,
            )
            mock_list.reset_mock()

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_detail_success(self, mock_list):
        """Verify --detail argument successfully pass detail to Client."""
        self.shell('host-list -r 1 --detail')
        mock_list.assert_called_once_with(
            detail=True,
            sort_dir='asc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_fields_success(self, mock_list):
        """Verify --fields argument successfully passed to Client."""
        self.shell('host-list -r 1 --fields id name')
        mock_list.assert_called_once_with(
            sort_dir='asc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_sort_key_field_key_success(self, mock_list):
        """Verify --sort-key arguments successfully passed to Client."""
        self.shell('host-list -r 1 --sort-key cell_id')
        mock_list.assert_called_once_with(
            sort_key='cell_id',
            sort_dir='asc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    def test_host_list_sort_key_invalid(self):
        """Verify --sort-key with invalid args, fails with Command Error."""
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'host-list -r 1 --sort-key invalid')

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_sort_dir_not_passed_without_sort_key(self, mock_list):
        """Verify --sort-dir arg ignored without --sort-key."""
        self.shell('host-list -r 1 --sort-dir desc')
        mock_list.assert_called_once_with(
            sort_dir='desc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_sort_dir_asc_success(self, mock_list):
        """Verify --sort-dir asc successfully passed to Client."""
        self.shell('host-list -r 1 --sort-key name --sort-dir asc')
        mock_list.assert_called_once_with(
            sort_key='name',
            sort_dir='asc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_sort_dir_desc_success(self, mock_list):
        """Verify --sort-dir desc successfully passed to Client."""
        self.shell('host-list -r 1 --sort-key name --sort-dir desc')
        mock_list.assert_called_once_with(
            sort_key='name',
            sort_dir='desc',
            region_id=1,
            marker=None,
            autopaginate=False,
        )

    def test_host_list_sort_dir_invalid_value(self):
        """Verify --sort-dir with invalid args, fails with Command Error."""
        (_, error) = self.shell(
            'host-list -r 1 --sort-key name --sort-dir invalid'
        )
        self.assertIn("invalid choice: 'invalid'", error)

    def test_host_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-create',
            '.*?^craton host-create: error:.*$'
        ]
        stdout, stderr = self.shell('host-create')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.create')
    def test_do_host_create_calls_host_manager_with_fields(self, mock_create):
        """Verify that do host create calls HostManager create."""
        client = mock.Mock()
        client.hosts = hosts.HostManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        hosts_shell.do_host_create(client, self.host_valid_fields)
        mock_create.assert_called_once_with(**self.host_valid_kwargs)

    @mock.patch('cratonclient.v1.hosts.HostManager.create')
    def test_do_host_create_ignores_unknown_fields(self, mock_create):
        """Verify that do host create ignores unknown field."""
        client = mock.Mock()
        client.hosts = hosts.HostManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        hosts_shell.do_host_create(client, self.host_invalid_fields)
        mock_create.assert_called_once_with(**self.host_valid_kwargs)

    def test_host_update_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-update',
            '.*?^craton host-update: error:.*$',
        ]
        stdout, stderr = self.shell('host-update')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.update')
    def test_do_host_update_calls_host_manager_with_fields(self, mock_update):
        """Verify that do host update calls HostManager update."""
        client = mock.Mock()
        client.hosts = hosts.HostManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        valid_input = Namespace(region=1,
                                id=1,
                                name='mock_host',
                                formatter=mock.Mock())
        hosts_shell.do_host_update(client, valid_input)
        mock_update.assert_called_once_with(1, name='mock_host')

    @mock.patch('cratonclient.v1.hosts.HostManager.update')
    def test_do_host_update_ignores_unknown_fields(self, mock_update):
        """Verify that do host update ignores unknown field."""
        client = mock.Mock()
        client.hosts = hosts.HostManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        invalid_input = Namespace(region=1,
                                  id=1,
                                  name='mock_host',
                                  formatter=mock.Mock(),
                                  invalid=True)
        hosts_shell.do_host_update(client, invalid_input)
        mock_update.assert_called_once_with(1, name='mock_host')

    def test_host_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-show',
            '.*?^craton host-show: error:.*$',
        ]
        stdout, stderr = self.shell('host-show')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.get')
    def test_do_host_show_calls_host_manager_with_fields(self, mock_get):
        """Verify that do host show calls HostManager get."""
        client = mock.Mock()
        client.hosts = hosts.HostManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        test_args = Namespace(id=1, region=1)
        formatter = test_args.formatter = mock.Mock()
        formatter.configure.return_value = formatter
        hosts_shell.do_host_show(client, test_args)
        mock_get.assert_called_once_with(vars(test_args)['id'])
        self.assertTrue(formatter.handle.called)
        self.assertEqual(1, formatter.handle.call_count)

    def test_host_delete_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-delete',
            '.*?^craton host-delete: error:.*$',
        ]
        stdout, stderr = self.shell('host-delete')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.delete')
    def test_do_host_delete_calls_host_manager_with_fields(self, mock_delete):
        """Verify that do host delete calls HostManager delete."""
        client = mock.Mock()
        client.hosts = hosts.HostManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        test_args = Namespace(id=1, region=1)
        hosts_shell.do_host_delete(client, test_args)
        mock_delete.assert_called_once_with(vars(test_args)['id'])
