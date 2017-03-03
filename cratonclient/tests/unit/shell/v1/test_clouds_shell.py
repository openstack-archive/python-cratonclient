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
"""Tests for the shell functions for the clouds resource."""
import mock

from cratonclient import exceptions
from cratonclient.shell.v1 import clouds_shell
from cratonclient.tests.unit.shell import base


class TestDoCloudShow(base.TestShellCommand):
    """Unit tests for the cloud-show command."""

    def test_prints_cloud_data(self):
        """Verify we print the data for the cloud."""
        args = self.args_for(id=1234)

        clouds_shell.do_cloud_show(self.craton_client, args)

        self.craton_client.clouds.get.assert_called_once_with(1234)
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)


class TestDoCloudCreate(base.TestShellCommand):
    """Unit tests for the cloud-create command."""

    def args_for(self, **kwargs):
        """Generate arguments for cloud-create."""
        kwargs.setdefault('name', 'New cloud')
        kwargs.setdefault('note', None)
        return super(TestDoCloudCreate, self).args_for(**kwargs)

    def test_accepts_only_required_arguments(self):
        """Verify operation with only --name provided."""
        args = self.args_for()

        clouds_shell.do_cloud_create(self.craton_client, args)

        self.craton_client.clouds.create.assert_called_once_with(
            name='New cloud',
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)

    def test_accepts_optional_arguments(self):
        """Verify operation with --note passed as well."""
        args = self.args_for(note='This is a note')

        clouds_shell.do_cloud_create(self.craton_client, args)

        self.craton_client.clouds.create.assert_called_once_with(
            name='New cloud',
            note='This is a note',
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)


class TestDoCloudUpdate(base.TestShellCommand):
    """Unit tests for cloud-update command."""

    def args_for(self, **kwargs):
        """Generate arguments for cloud-update."""
        kwargs.setdefault('id', 12345)
        kwargs.setdefault('name', None)
        kwargs.setdefault('note', None)
        return super(TestDoCloudUpdate, self).args_for(**kwargs)

    def test_nothing_to_update_raises_error(self):
        """Verify specifying nothing raises a CommandError."""
        args = self.args_for()

        self.assertRaisesCommandErrorWith(
            clouds_shell.do_cloud_update,
            args,
        )
        self.assertNothingWasCalled()

    def test_name_is_updated(self):
        """Verify the name attribute update is sent."""
        args = self.args_for(name='A New Name')

        clouds_shell.do_cloud_update(self.craton_client, args)

        self.craton_client.clouds.update.assert_called_once_with(
            12345,
            name='A New Name',
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)

    def test_note_is_updated(self):
        """Verify the note attribute is updated."""
        args = self.args_for(note='A New Note')

        clouds_shell.do_cloud_update(self.craton_client, args)

        self.craton_client.clouds.update.assert_called_once_with(
            12345,
            note='A New Note',
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)

    def test_everything_is_updated(self):
        """Verify the note and name are updated."""
        args = self.args_for(
            note='A New Note',
            name='A New Name',
        )

        clouds_shell.do_cloud_update(self.craton_client, args)

        self.craton_client.clouds.update.assert_called_once_with(
            12345,
            note='A New Note',
            name='A New Name',
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)


class TestDoCloudDelete(base.TestShellCommand):
    """Unit tests for the cloud-delete command."""

    def setUp(self):
        """Mock the print function."""
        super(TestDoCloudDelete, self).setUp()
        self.print_mock = mock.patch(
            'cratonclient.shell.v1.clouds_shell.print'
        )
        self.print_func = self.print_mock.start()

    def tearDown(self):
        """Clean up our print function mock."""
        super(TestDoCloudDelete, self).tearDown()
        self.print_mock.stop()

    def args_for(self, **kwargs):
        """Generate args for the cloud-delete command."""
        kwargs.setdefault('id', 123456)
        return super(TestDoCloudDelete, self).args_for(**kwargs)

    def test_successful(self):
        """Verify successful deletion."""
        self.craton_client.clouds.delete.return_value = True
        args = self.args_for()

        clouds_shell.do_cloud_delete(self.craton_client, args)

        self.craton_client.clouds.delete.assert_called_once_with(123456)
        self.print_func.assert_called_once_with(
            'Cloud 123456 was successfully deleted.'
        )

    def test_failed(self):
        """Verify failed deletion."""
        self.craton_client.clouds.delete.return_value = False
        args = self.args_for()

        clouds_shell.do_cloud_delete(self.craton_client, args)

        self.craton_client.clouds.delete.assert_called_once_with(123456)
        self.print_func.assert_called_once_with(
            'Cloud 123456 was not deleted.'
        )

    def test_failed_with_exception(self):
        """Verify we raise a CommandError on client exceptions."""
        self.craton_client.clouds.delete.side_effect = exceptions.NotFound
        args = self.args_for()

        self.assertRaisesCommandErrorWith(clouds_shell.do_cloud_delete, args)

        self.craton_client.clouds.delete.assert_called_once_with(123456)
        self.assertFalse(self.print_func.called)


class TestDoCloudList(base.TestShellCommand):
    """Test cloud-list command."""

    def args_for(self, **kwargs):
        """Generate the default argument list for cloud-list."""
        kwargs.setdefault('detail', False)
        kwargs.setdefault('limit', None)
        kwargs.setdefault('fields', clouds_shell.DEFAULT_CLOUD_FIELDS)
        kwargs.setdefault('marker', None)
        kwargs.setdefault('all', False)
        return super(TestDoCloudList, self).args_for(**kwargs)

    def test_with_defaults(self):
        """Test cloud-list with default values."""
        args = self.args_for()
        clouds_shell.do_cloud_list(self.craton_client, args)

        self.assertFieldsEqualTo(clouds_shell.DEFAULT_CLOUD_FIELDS)

    def test_negative_limit(self):
        """Ensure we raise an exception for negative limits."""
        args = self.args_for(limit=-1)
        self.assertRaisesCommandErrorWith(clouds_shell.do_cloud_list, args)

    def test_positive_limit(self):
        """Verify that we pass positive limits to the call to list."""
        args = self.args_for(limit=5)
        clouds_shell.do_cloud_list(self.craton_client, args)
        self.craton_client.clouds.list.assert_called_once_with(
            limit=5,
            marker=None,
            autopaginate=False,
        )
        self.assertFieldsEqualTo(clouds_shell.DEFAULT_CLOUD_FIELDS)

    def test_fields(self):
        """Verify that we print out specific fields."""
        args = self.args_for(fields=['id', 'name', 'note'])
        clouds_shell.do_cloud_list(self.craton_client, args)
        self.assertFieldsEqualTo(['id', 'name', 'note'])

    def test_invalid_fields(self):
        """Verify that we error out with invalid fields."""
        args = self.args_for(fields=['uuid', 'not-name', 'nate'])
        self.assertRaisesCommandErrorWith(clouds_shell.do_cloud_list, args)
        self.assertNothingWasCalled()

    def test_autopagination(self):
        """Verify autopagination is controlled by --all."""
        args = self.args_for(all=True)

        clouds_shell.do_cloud_list(self.craton_client, args)

        self.craton_client.clouds.list.assert_called_once_with(
            limit=100,
            marker=None,
            autopaginate=True,
        )

    def test_autopagination_overrides_limit(self):
        """Verify --all overrides --limit."""
        args = self.args_for(all=True, limit=35)

        clouds_shell.do_cloud_list(self.craton_client, args)

        self.craton_client.clouds.list.assert_called_once_with(
            limit=100,
            marker=None,
            autopaginate=True,
        )

    def test_marker_pass_through(self):
        """Verify we pass our marker through to the client."""
        args = self.args_for(marker=31)

        clouds_shell.do_cloud_list(self.craton_client, args)

        self.craton_client.clouds.list.assert_called_once_with(
            marker=31,
            autopaginate=False,
        )
