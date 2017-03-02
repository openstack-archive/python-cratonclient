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
"""Tests for the shell functions for the hosts resource."""
import mock

from cratonclient import exceptions
from cratonclient.shell.v1 import hosts_shell
from cratonclient.tests.unit.shell import base


class TestDoHostShow(base.TestShellCommandUsingPrintDict):
    """Unit tests for the host show command."""

    def test_print_host_data(self):
        """Verify we print info for the specified host."""
        args = self.args_for(
            region=135,
            id=246,
        )

        hosts_shell.do_host_show(self.craton_client, args)

        self.craton_client.hosts.get.assert_called_once_with(246)


class TestDoHostList(base.TestShellCommandUsingPrintList):
    """Unit tests for the host list command."""

    def args_for(self, **kwargs):
        """Generate a Namespace for do_host_list."""
        kwargs.setdefault('cloud', None)
        kwargs.setdefault('region', 246)
        kwargs.setdefault('cell', None)
        kwargs.setdefault('detail', False)
        kwargs.setdefault('limit', None)
        kwargs.setdefault('sort_key', None)
        kwargs.setdefault('sort_dir', 'asc')
        kwargs.setdefault('fields', hosts_shell.DEFAULT_HOST_FIELDS)
        kwargs.setdefault('marker', None)
        kwargs.setdefault('all', False)
        kwargs.setdefault('vars', None)
        kwargs.setdefault('label', None)
        kwargs.setdefault('device_type', None)
        kwargs.setdefault('ip', None)
        return super(TestDoHostList, self).args_for(**kwargs)

    def test_only_required_parameters(self):
        """Verify the behaviour with the minimum number of params."""
        args = self.args_for()

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name'
        ])

    def test_with_cell_id(self):
        """Verify that we include the cell_id in the params."""
        args = self.args_for(cell=789)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            cell_id=789,
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name',
        ])

    def test_with_cloud_id(self):
        """Verify that we include the cell_id in the params."""
        args = self.args_for(cloud=123)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            sort_dir='asc',
            cloud_id=123,
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name',
        ])

    def test_with_detail(self):
        """Verify the behaviour of specifying --detail."""
        args = self.args_for(detail=True)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            detail=True,
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active',
            'cell_id',
            'cloud_id',
            'created_at',
            'device_type',
            'id',
            'ip_address',
            'labels',
            'name',
            'note',
            'parent_id',
            'project_id',
            'region_id',
            'updated_at',
        ])

    def test_with_limit(self):
        """Verify the behaviour with --limit specified."""
        args = self.args_for(limit=20)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            limit=20,
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name'
        ])

    def test_negative_limit_raises_command_error(self):
        """Verify that we forbid negative limit values."""
        args = self.args_for(limit=-10)

        self.assertRaisesCommandErrorWith(hosts_shell.do_host_list, args)
        self.assertNothingWasCalled()

    def test_with_vars(self):
        """Verify the behaviour with --vars specified."""
        args = self.args_for(vars='a:b')

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            vars='a:b',
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(hosts_shell.DEFAULT_HOST_FIELDS)

    def test_with_label(self):
        """Verify the behaviour with --label specified."""
        args = self.args_for(label='compute')

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            label='compute',
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name'
        ])

    def test_with_device_type(self):
        """Verify the behaviour with --device-type specified."""
        args = self.args_for(device_type='compute')

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            device_type='compute',
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name'
        ])

    def test_with_ip(self):
        """Verify the behaviour with --ip specified."""
        args = self.args_for(ip='10.10.1.1')

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            ip_address='10.10.1.1',
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'active', 'cell_id', 'device_type', 'id', 'name'
        ])

    def test_fields(self):
        """Verify that we can specify custom fields."""
        args = self.args_for(fields=['id', 'name', 'cell_id'])

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )
        self.assertSortedPrintListFieldsEqualTo([
            'cell_id', 'id', 'name',
        ])

    def test_invalid_sort_key(self):
        """Verify that we disallow invalid sort keys."""
        args = self.args_for(sort_key='my-fake-sort-key')

        self.assertRaisesCommandErrorWith(
            hosts_shell.do_host_list, args
        )
        self.assertNothingWasCalled()

    def test_sort_key(self):
        """Verify we pass sort_key to our list call."""
        args = self.args_for(sort_key='ip_address')

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            sort_key='ip_address',
            sort_dir='asc',
            region_id=246,
            autopaginate=False,
            marker=None,
        )

    def test_fields_and_detail_raise_command_error(self):
        """Verify combining fields and detail cause an error."""
        args = self.args_for(detail=True, fields=['id', 'name', 'ip_address'])

        self.assertRaisesCommandErrorWith(
            hosts_shell.do_host_list, args,
        )
        self.assertNothingWasCalled()

    def test_invalid_fields_raise_command_error(self):
        """Verify sending an invalid field raises a CommandError."""
        args = self.args_for(fields=['fake-field', 'id'])

        self.assertRaisesCommandErrorWith(
            hosts_shell.do_host_list, args,
        )
        self.assertNothingWasCalled()

    def test_autopagination(self):
        """Verify autopagination is controlled by --all."""
        args = self.args_for(all=True)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            region_id=246,
            sort_dir='asc',
            limit=100,
            marker=None,
            autopaginate=True,
        )

    def test_autopagination_overrides_limit(self):
        """Verify --all overrides --limit."""
        args = self.args_for(all=True, limit=30)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            region_id=246,
            sort_dir='asc',
            limit=100,
            marker=None,
            autopaginate=True,
        )

    def test_marker_pass_through(self):
        """Verify we pass our marker through to the client."""
        args = self.args_for(marker=42)

        hosts_shell.do_host_list(self.craton_client, args)

        self.craton_client.hosts.list.assert_called_once_with(
            region_id=246,
            sort_dir='asc',
            marker=42,
            autopaginate=False,
        )


class TestDoHostCreate(base.TestShellCommandUsingPrintDict):
    """Tests for the do_host_create shell command."""

    def args_for(self, **kwargs):
        """Generate the Namespace object needed for host create."""
        kwargs.setdefault('region', 123)
        kwargs.setdefault('name', 'test-hostname')
        kwargs.setdefault('ip_address', '10.0.1.10')
        kwargs.setdefault('region_id', 123)
        kwargs.setdefault('cell_id', 246)
        kwargs.setdefault('device_type', 'host')
        kwargs.setdefault('active', True)
        kwargs.setdefault('note', None)
        kwargs.setdefault('labels', [])
        return super(TestDoHostCreate, self).args_for(**kwargs)

    def test_only_the_required_arguments(self):
        """Verify that the required arguments are passed appropriately."""
        args = self.args_for()

        hosts_shell.do_host_create(self.craton_client, args)

        self.craton_client.hosts.create.assert_called_once_with(
            name='test-hostname',
            ip_address='10.0.1.10',
            cell_id=246,
            device_type='host',
            active=True,
            region_id=123,
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.create.return_value
        )

    def test_with_a_note(self):
        """Verify that we pass along the note."""
        args = self.args_for(note='This is a note.')

        hosts_shell.do_host_create(self.craton_client, args)

        self.craton_client.hosts.create.assert_called_once_with(
            name='test-hostname',
            ip_address='10.0.1.10',
            cell_id=246,
            device_type='host',
            active=True,
            region_id=123,
            note='This is a note.',
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.create.return_value
        )

    def test_with_labels(self):
        """Verify that we pass along our labels."""
        args = self.args_for(labels=['label-0', 'label-1'])

        hosts_shell.do_host_create(self.craton_client, args)

        self.craton_client.hosts.create.assert_called_once_with(
            name='test-hostname',
            ip_address='10.0.1.10',
            cell_id=246,
            device_type='host',
            active=True,
            region_id=123,
            labels=['label-0', 'label-1'],
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.create.return_value
        )


class TestDoHostUpdate(base.TestShellCommandUsingPrintDict):
    """Tests host-update shell command."""

    def setUp(self):
        """Also patch out the print function."""
        super(TestDoHostUpdate, self).setUp()
        self.print_mocker = mock.patch(
            'cratonclient.shell.v1.hosts_shell.print'
        )
        self.print_mock = self.print_mocker.start()
        self.craton_client.hosts.update.return_value = mock.Mock(id=246)

    def tearDown(self):
        """Stop mocking print."""
        super(TestDoHostUpdate, self).tearDown()
        self.print_mocker.stop()

    def args_for(self, **kwargs):
        """Generate arguments for host-update command."""
        kwargs.setdefault('region', 123)
        kwargs.setdefault('id', 246)
        kwargs.setdefault('name', None)
        kwargs.setdefault('ip_address', None)
        kwargs.setdefault('region_id', None)
        kwargs.setdefault('cell_id', None)
        kwargs.setdefault('active', True)
        kwargs.setdefault('note', None)
        kwargs.setdefault('labels', [])
        return super(TestDoHostUpdate, self).args_for(**kwargs)

    def test_with_basic_required_parameters(self):
        """Verify the basic update call works."""
        args = self.args_for()

        hosts_shell.do_host_update(self.craton_client, args)

        self.craton_client.hosts.update.assert_called_once_with(
            246,
            active=True,
        )
        self.print_mock.assert_called_once_with(
            'Host 246 has been successfully updated.'
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.update.return_value
        )

    def test_with_name(self):
        """Verify the new name is passed along."""
        args = self.args_for(name='New name')

        hosts_shell.do_host_update(self.craton_client, args)

        self.craton_client.hosts.update.assert_called_once_with(
            246,
            name='New name',
            active=True,
        )
        self.print_mock.assert_called_once_with(
            'Host 246 has been successfully updated.'
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.update.return_value
        )

    def test_with_ip_address(self):
        """Verify the new IP Address is passed along."""
        args = self.args_for(ip_address='10.1.0.10')

        hosts_shell.do_host_update(self.craton_client, args)

        self.craton_client.hosts.update.assert_called_once_with(
            246,
            ip_address='10.1.0.10',
            active=True,
        )
        self.print_mock.assert_called_once_with(
            'Host 246 has been successfully updated.'
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.update.return_value
        )

    def test_disable_host(self):
        """Verify active is passed even when False."""
        args = self.args_for(active=False)

        hosts_shell.do_host_update(self.craton_client, args)

        self.craton_client.hosts.update.assert_called_once_with(
            246,
            active=False,
        )
        self.print_mock.assert_called_once_with(
            'Host 246 has been successfully updated.'
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.update.return_value
        )

    def test_optional_parameters(self):
        """Verify all optional parameters are passed along when specified."""
        args = self.args_for(
            name='New name',
            ip_address='10.1.1.1',
            region_id=789,
            cell_id=101,
            note='A note about a host',
            labels=['label1', 'label2'],
        )

        hosts_shell.do_host_update(self.craton_client, args)

        self.craton_client.hosts.update.assert_called_once_with(
            246,
            active=True,
            name='New name',
            ip_address='10.1.1.1',
            region_id=789,
            cell_id=101,
            note='A note about a host',
            labels=['label1', 'label2'],
        )
        self.print_mock.assert_called_once_with(
            'Host 246 has been successfully updated.'
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.formatter.handle.assert_called_once_with(
            self.craton_client.hosts.update.return_value
        )


class TestDoHostDelete(base.TestShellCommand):
    """Tests for the host-delete shell command."""

    def setUp(self):
        """Set-up a print function mock."""
        super(TestDoHostDelete, self).setUp()
        self.print_mocker = mock.patch(
            'cratonclient.shell.v1.hosts_shell.print'
        )
        self.print_mock = self.print_mocker.start()

    def tearDown(self):
        """Clean up the print function mock."""
        super(TestDoHostDelete, self).tearDown()
        self.print_mocker.stop()

    def test_successful(self):
        """Verify we print our successful message."""
        self.craton_client.hosts.delete.return_value = True
        args = self.args_for(
            region=123,
            id=246,
        )

        hosts_shell.do_host_delete(self.craton_client, args)

        self.craton_client.hosts.delete.assert_called_once_with(246)
        self.print_mock.assert_called_once_with(
            'Host 246 was successfully deleted.'
        )

    def test_failed(self):
        """Verify the message we print when deletion fails."""
        self.craton_client.hosts.delete.return_value = False
        args = self.args_for(
            region=123,
            id=246,
        )

        hosts_shell.do_host_delete(self.craton_client, args)

        self.craton_client.hosts.delete.assert_called_once_with(246)
        self.print_mock.assert_called_once_with(
            'Host 246 was not deleted.'
        )

    def test_failed_with_exception(self):
        """Verify we raise a CommandError on client exceptions."""
        self.craton_client.hosts.delete.side_effect = exceptions.NotFound
        args = self.args_for(
            region=123,
            id=246,
        )

        self.assertRaisesCommandErrorWith(hosts_shell.do_host_delete, args)

        self.craton_client.hosts.delete.assert_called_once_with(246)
        self.assertFalse(self.print_mock.called)
