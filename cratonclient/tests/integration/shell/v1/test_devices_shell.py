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

"""Tests for `cratonclient.shell.v1.devices_shell` module."""

import mock
import re

from cratonclient import exceptions as exc
from cratonclient.tests.integration.shell import base


class TestDevicesShell(base.ShellTestCase):
    """Test our craton devices shell commands."""

    re_options = re.DOTALL | re.MULTILINE

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_success(self, mock_list):
        """Verify that no arguments prints out all project devices."""
        self.shell('device-list')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_parse_param_success(self, mock_list):
        """Verify that success of parsing a subcommand argument."""
        self.shell('device-list --limit 0')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_limit_0_success(self, mock_list):
        """Verify that --limit 0 prints out all project devices."""
        self.shell('device-list --limit 0')
        mock_list.assert_called_once_with(
            limit=0,
            sort_dir='asc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_limit_positive_num_success(self, mock_list):
        """Verify --limit X, where X is a positive integer, succeeds.

        The command will print out X number of project devices.
        """
        self.shell('device-list --limit 1')
        mock_list.assert_called_once_with(
            limit=1,
            sort_dir='asc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    def test_device_list_limit_negative_num_failure(self):
        """Verify --limit X, where X is a negative integer, fails.

        The command will cause a Command Error message response.
        """
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'device-list -r 1 --limit -1')

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_cell_success(self, mock_list):
        """Verify --cell arguments successfully pass cell to Client."""
        for cell_arg in ['-c', '--cell']:
            self.shell('device-list {0} 1'.format(cell_arg))
            mock_list.assert_called_once_with(
                cell_id=1,
                sort_dir='asc',
                descendants=False,
                marker=None,
                autopaginate=False,
            )
            mock_list.reset_mock()

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_fields_success(self, mock_list):
        """Verify --fields argument successfully passed to Client."""
        self.shell('device-list --fields id name')
        mock_list.assert_called_once_with(
            sort_dir='asc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_sort_keys_field_key_success(self, mock_list):
        """Verify --sort-key arguments successfully passed to Client."""
        self.shell('device-list --sort-key cell_id')
        mock_list.assert_called_once_with(
            sort_keys='cell_id',
            sort_dir='asc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    def test_device_list_sort_keys_invalid(self):
        """Verify --sort-key with invalid args, fails with Command Error."""
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'device-list --sort-key invalid')

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_sort_dir_not_passed_without_sort_key(self, mock_list):
        """Verify --sort-dir arg ignored without --sort-key."""
        self.shell('device-list --sort-dir desc')
        mock_list.assert_called_once_with(
            sort_dir='desc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_sort_dir_asc_success(self, mock_list):
        """Verify --sort-dir asc successfully passed to Client."""
        self.shell('device-list --sort-key name --sort-dir asc')
        mock_list.assert_called_once_with(
            sort_keys='name',
            sort_dir='asc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_sort_dir_desc_success(self, mock_list):
        """Verify --sort-dir desc successfully passed to Client."""
        self.shell('device-list --sort-key name --sort-dir desc')
        mock_list.assert_called_once_with(
            sort_keys='name',
            sort_dir='desc',
            descendants=False,
            marker=None,
            autopaginate=False,
        )

    def test_device_list_sort_dir_invalid_value(self):
        """Verify --sort-dir with invalid args, fails with Command Error."""
        (_, error) = self.shell(
            'device-list -r 1 --sort-key name --sort-dir invalid'
        )
        self.assertIn("invalid choice: 'invalid'", error)

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_filter_by_parent_success(self, mock_list):
        """Verify --parent ID successfully passed to Client."""
        self.shell('device-list --parent 12345')
        mock_list.assert_called_once_with(
            sort_dir='asc',
            descendants=False,
            parent_id=12345,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.devices.DeviceManager.list')
    def test_device_list_filter_by_parent_descendants_success(self, mock_list):
        """Verify --parent ID successfully passed to Client."""
        self.shell('device-list --parent 12345 --descendants')
        mock_list.assert_called_once_with(
            sort_dir='asc',
            parent_id=12345,
            descendants=True,
            marker=None,
            autopaginate=False,
        )
