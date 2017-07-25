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
"""Tests for the shell functions for the projects resource."""

import mock

from cratonclient import exceptions
from cratonclient.shell.v1 import projects_shell
from cratonclient.tests.unit.shell import base

from oslo_utils import uuidutils


class TestDoShellShow(base.TestShellCommand):
    """Unit tests for the project show command."""

    def test_simple_usage(self):
        """Verify the behaviour of do_project_show."""
        args = self.args_for(
            region=123,
            id=456,
        )

        projects_shell.do_project_show(self.craton_client, args)

        self.craton_client.projects.get.assert_called_once_with(456)
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)


class TestDoProjectList(base.TestShellCommand):
    """Unit tests for the project list command."""

    def assertNothingWasCalled(self):
        """Assert inventory, list, and print_list were not called."""
        super(TestDoProjectList, self).assertNothingWasCalled()
        self.assertFalse(self.formatter.configure.called)
        self.assertFalse(self.formatter.handle.called)

    def args_for(self, **kwargs):
        """Generate the default argument list for project-list."""
        kwargs.setdefault('name', None)
        kwargs.setdefault('limit', None)
        kwargs.setdefault('detail', False)
        kwargs.setdefault('fields', projects_shell.DEFAULT_PROJECT_FIELDS)
        kwargs.setdefault('marker', None)
        kwargs.setdefault('all', False)
        return super(TestDoProjectList, self).args_for(**kwargs)

    def test_with_defaults(self):
        """Verify behaviour of do_project_list with mostly default values."""
        args = self.args_for()

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            marker=None,
            autopaginate=False,
        )
        self.assertFieldsEqualTo(projects_shell.DEFAULT_PROJECT_FIELDS)

    def test_negative_limit(self):
        """Ensure we raise an exception for negative limits."""
        args = self.args_for(limit=-1)

        self.assertRaisesCommandErrorWith(projects_shell.do_project_list,
                                          args)
        self.assertNothingWasCalled()

    def test_positive_limit(self):
        """Verify that we pass positive limits to the call to list."""
        args = self.args_for(limit=5)

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            limit=5,
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(projects_shell.DEFAULT_PROJECT_FIELDS)

    def test_detail(self):
        """Verify the behaviour of specifying --detail."""
        args = self.args_for(detail=True)

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            marker=None,
            autopaginate=False,
        )
        self.assertFieldsEqualTo(projects_shell.PROJECT_FIELDS)

    def test_list_name(self):
        """Verify the behaviour of specifying --detail."""
        args = self.args_for(name='project_1')

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            name='project_1',
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(projects_shell.DEFAULT_PROJECT_FIELDS)

    def test_raises_exception_with_detail_and_fields(self):
        """Verify that we fail when users specify --detail and --fields."""
        args = self.args_for(
            detail=True,
            fields=['name', 'id'],
        )

        self.assertRaisesCommandErrorWith(projects_shell.do_project_list, args)
        self.assertNothingWasCalled()

    def test_fields(self):
        """Verify that we print out specific fields."""
        args = self.args_for(fields=['name', 'id'])

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            autopaginate=False,
            marker=None,
        )
        self.assertFieldsEqualTo(['name', 'id'])

    def test_invalid_fields(self):
        """Verify that we error out with invalid fields."""
        args = self.args_for(fields=['uuid', 'not-name', 'nate'])

        self.assertRaisesCommandErrorWith(projects_shell.do_project_list, args)
        self.assertNothingWasCalled()

    def test_autopagination(self):
        """Verify autopagination is controlled by --all."""
        args = self.args_for(all=True)

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            limit=100,
            autopaginate=True,
            marker=None,
        )

    def test_autopagination_overrides_limit(self):
        """Verify --all overrides --limit."""
        args = self.args_for(all=True, limit=25)

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            limit=100,
            autopaginate=True,
            marker=None,
        )

    def test_marker_support(self):
        """Verify we pass through the marker."""
        project_id = uuidutils.generate_uuid()
        args = self.args_for(marker=project_id)

        projects_shell.do_project_list(self.craton_client, args)

        self.craton_client.projects.list.assert_called_once_with(
            autopaginate=False,
            marker=project_id,
        )


class TestDoProjectCreate(base.TestShellCommand):
    """Unit tests for the project create command."""

    def args_for(self, **kwargs):
        """Generate the default args for project-create."""
        kwargs.setdefault('name', 'New Project')
        return super(TestDoProjectCreate, self).args_for(**kwargs)

    def test_create(self):
        """Verify our parameters to projects.create."""
        args = self.args_for()

        projects_shell.do_project_create(self.craton_client, args)

        self.craton_client.projects.create.assert_called_once_with(
            name='New Project'
        )
        self.formatter.configure.assert_called_once_with(wrap=72)
        self.assertEqual(1, self.formatter.handle.call_count)


class TestDoProjectDelete(base.TestShellCommand):
    """Tests for the do_project_delete command."""

    def setUp(self):
        """Initialize our print mock."""
        super(TestDoProjectDelete, self).setUp()
        self.print_func_mock = mock.patch(
            'cratonclient.shell.v1.projects_shell.print'
        )
        self.print_func = self.print_func_mock.start()
        self.project_id = uuidutils.generate_uuid()

    def tearDown(self):
        """Clean up our print mock."""
        super(TestDoProjectDelete, self).tearDown()
        self.print_func_mock.stop()

    def test_successful(self):
        """Verify the message we print when successful."""
        self.craton_client.projects.delete.return_value = True
        args = self.args_for(
            id=self.project_id,
        )

        projects_shell.do_project_delete(self.craton_client, args)

        self.craton_client.projects.delete.assert_called_once_with(
            self.project_id)
        self.print_func.assert_called_once_with(
            'Project {} was successfully deleted.'.format(self.project_id)
        )

    def test_failed(self):
        """Verify the message we print when deletion fails."""
        self.craton_client.projects.delete.return_value = False
        args = self.args_for(
            id=self.project_id,
        )

        projects_shell.do_project_delete(self.craton_client, args)

        self.craton_client.projects.delete.assert_called_once_with(
            self.project_id)
        self.print_func.assert_called_once_with(
            'Project {} was not deleted.'.format(self.project_id)
        )

    def test_failed_with_exception(self):
        """Verify the message we print when deletion fails."""
        self.craton_client.projects.delete.side_effect = exceptions.NotFound
        args = self.args_for(
            region=123,
            id=self.project_id,
        )

        self.assertRaisesCommandErrorWith(projects_shell.do_project_delete,
                                          args)

        self.craton_client.projects.delete.assert_called_once_with(
            self.project_id)
        self.assertFalse(self.print_func.called)
