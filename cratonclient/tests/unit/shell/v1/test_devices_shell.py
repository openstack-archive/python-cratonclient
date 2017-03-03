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
"""Tests for the shell functions for the devices resource."""
from cratonclient.shell.v1 import devices_shell
from cratonclient.tests.unit.shell import base


class TestDoDeviceList(base.TestShellCommandUsingPrintList):
    """Unit tests for the device list command."""

    def args_for(self, **kwargs):
        """Generate a Namespace for do_device_list."""
        kwargs.setdefault('detail', False)
        kwargs.setdefault('cloud', None)
        kwargs.setdefault('region', None)
        kwargs.setdefault('cell', None)
        kwargs.setdefault('parent', None)
        kwargs.setdefault('descendants', False)
        kwargs.setdefault('active', None)
        kwargs.setdefault('limit', None)
        kwargs.setdefault('sort_key', None)
        kwargs.setdefault('sort_dir', 'asc')
        kwargs.setdefault('fields', devices_shell.DEFAULT_DEVICE_FIELDS)
        kwargs.setdefault('marker', None)
        kwargs.setdefault('all', False)
        return super(TestDoDeviceList, self).args_for(**kwargs)

    def test_only_required_parameters(self):
        """Verify the behaviour with the minimum number of params."""
        args = self.args_for()

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_with_parent_id(self):
        """Verify that we include the parent_id in the params."""
        args = self.args_for(parent=789)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            parent_id=789,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_with_parent_id_and_descendants(self):
        """Verify that the parent_id and descendants is in the params."""
        args = self.args_for(parent=789, descendants=False)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            parent_id=789,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_with_region_id(self):
        """Verify that we include the region_id in the params."""
        args = self.args_for(region=789)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            region_id=789,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_with_cell_id(self):
        """Verify that we include the cell_id in the params."""
        args = self.args_for(cell=789)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            cell_id=789,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_with_cloud_id(self):
        """Verify that we include the cell_id in the params."""
        args = self.args_for(cloud=123)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_dir='asc',
            cloud_id=123,
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_with_limit(self):
        """Verify the behaviour with --limit specified."""
        args = self.args_for(limit=20)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            limit=20,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(devices_shell.DEFAULT_DEVICE_FIELDS)

    def test_negative_limit_raises_command_error(self):
        """Verify that we forbid negative limit values."""
        args = self.args_for(limit=-10)

        self.assertRaisesCommandErrorWith(devices_shell.do_device_list, args)
        self.assertNothingWasCalled()

    def test_fields(self):
        """Verify that we can specify custom fields."""
        args = self.args_for(fields=['id', 'name', 'cell_id'])

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(['id', 'name', 'cell_id'])

    def test_invalid_sort_key(self):
        """Verify that we disallow invalid sort keys."""
        args = self.args_for(sort_key='my-fake-sort-key')

        self.assertRaisesCommandErrorWith(
            devices_shell.do_device_list, args
        )
        self.assertNothingWasCalled()

    def test_sort_key(self):
        """Verify we pass sort_key to our list call."""
        args = self.args_for(sort_key='ip_address')

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_keys='ip_address',
            sort_dir='asc',
            autopaginate=False,
            marker=None,
        )

    def test_invalid_fields_raise_command_error(self):
        """Verify sending an invalid field raises a CommandError."""
        args = self.args_for(fields=['fake-field', 'id'])

        self.assertRaisesCommandErrorWith(
            devices_shell.do_device_list, args,
        )
        self.assertNothingWasCalled()

    def test_autopagination(self):
        """Verify autopagination is controlled by --all."""
        args = self.args_for(all=True)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_dir='asc',
            limit=100,
            marker=None,
            autopaginate=True,
        )

    def test_autopagination_overrides_limit(self):
        """Verify --all overrides --limit."""
        args = self.args_for(all=True, limit=30)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_dir='asc',
            limit=100,
            marker=None,
            autopaginate=True,
        )

    def test_marker_pass_through(self):
        """Verify we pass our marker through to the client."""
        args = self.args_for(marker=42)

        devices_shell.do_device_list(self.craton_client, args)

        self.craton_client.devices.list.assert_called_once_with(
            descendants=False,
            sort_dir='asc',
            marker=42,
            autopaginate=False,
        )
