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

"""Tests for `cratonclient.shell.v1.projects_shell` module."""

import mock
import re

from argparse import Namespace
from testtools import matchers

from cratonclient import exceptions as exc
from cratonclient.shell.v1 import projects_shell
from cratonclient.tests.integration import base
from cratonclient.v1 import projects


class TestProjectsShell(base.ShellTestCase):
    """Test our craton projects shell commands."""

    re_options = re.DOTALL | re.MULTILINE
    project_valid_fields = None
    project_invalid_field = None

    def setUp(self):
        """Setup required test fixtures."""
        super(TestProjectsShell, self).setUp()
        self.project_valid_fields = Namespace(name='mock_project')
        self.project_invalid_field = Namespace(name='mock_project',
                                               invalid_foo='ignored')

    @mock.patch('cratonclient.v1.projects.ProjectManager.list')
    def test_project_list_success(self, mock_list):
        """Verify that no arguments prints out all project projects."""
        self.shell('project-list')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.projects.ProjectManager.list')
    def test_project_list_parse_param_success(self, mock_list):
        """Verify that success of parsing a subcommand argument."""
        self.shell('project-list --limit 0')
        self.assertTrue(mock_list.called)

    @mock.patch('cratonclient.v1.projects.ProjectManager.list')
    def test_project_list_limit_0_success(self, mock_list):
        """Verify that --limit 0 prints out all project projects."""
        self.shell('project-list --limit 0')
        mock_list.assert_called_once_with(
            limit=0,
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.projects.ProjectManager.list')
    def test_project_list_limit_positive_num_success(self, mock_list):
        """Verify --limit X, where X is a positive integer, succeeds.

        The command will print out X number of project projects.
        """
        self.shell('project-list --limit 1')
        mock_list.assert_called_once_with(
            limit=1,
            marker=None,
            autopaginate=False,
        )

    def test_project_list_limit_negative_num_failure(self):
        """Verify --limit X, where X is a negative integer, fails.

        The command will cause a Command Error message response.
        """
        self.assertRaises(exc.CommandError,
                          self.shell,
                          'project-list --limit -1')

    @mock.patch('cratonclient.v1.projects.ProjectManager.list')
    def test_project_list_detail_success(self, mock_list):
        """Verify --detail argument successfully pass detail to Client."""
        self.shell('project-list --detail')
        mock_list.assert_called_once_with(
            marker=None,
            autopaginate=False,
        )

    @mock.patch('cratonclient.v1.projects.ProjectManager.list')
    @mock.patch('cratonclient.common.cliutils.print_list')
    def test_project_list_fields_success(self, mock_printlist, mock_list):
        """Verify --fields argument successfully passed to Client."""
        self.shell('project-list --fields id name')
        mock_list.assert_called_once_with(
            marker=None,
            autopaginate=False,
        )
        mock_printlist.assert_called_once_with(mock.ANY,
                                               list({'id': 'ID',
                                                     'name': 'Name'}))

    def test_project_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton project-create',
            '.*?^craton project-create: error:.*$'
        ]
        stdout, stderr = self.shell('project-create')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.projects.ProjectManager.create')
    def test_do_project_create_calls_project_manager_with_fields(self,
                                                                 mock_create):
        """Verify that do project create calls ProjectManager create."""
        client = mock.Mock()
        client.projects = projects.ProjectManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        projects_shell.do_project_create(client, self.project_valid_fields)
        mock_create.assert_called_once_with(**vars(self.project_valid_fields))

    @mock.patch('cratonclient.v1.projects.ProjectManager.create')
    def test_do_project_create_ignores_unknown_fields(self, mock_create):
        """Verify that do project create ignores unknown field."""
        client = mock.Mock()
        client.projects = projects.ProjectManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        projects_shell.do_project_create(client, self.project_invalid_field)
        mock_create.assert_called_once_with(**vars(self.project_valid_fields))

    def test_project_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton project-show',
            '.*?^craton project-show: error:.*$',
        ]
        stdout, stderr = self.shell('project-show')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.projects.ProjectManager.get')
    def test_do_project_show_calls_project_manager_with_fields(self, mock_get):
        """Verify that do project show calls ProjectManager get."""
        client = mock.Mock()
        client.projects = projects.ProjectManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        test_args = Namespace(id=1)
        projects_shell.do_project_show(client, test_args)
        mock_get.assert_called_once_with(vars(test_args)['id'])

    def test_project_delete_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton project-delete',
            '.*?^craton project-delete: error:.*$',
        ]
        stdout, stderr = self.shell('project-delete')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.projects.ProjectManager.delete')
    def test_do_project_delete_calls_project_manager_with_fields(self,
                                                                 mock_delete):
        """Verify that do project delete calls ProjectManager delete."""
        client = mock.Mock()
        client.projects = projects.ProjectManager(
            mock.ANY, 'http://127.0.0.1/',
            region_id=mock.ANY,
        )
        test_args = Namespace(id=1, region=1)
        projects_shell.do_project_delete(client, test_args)
        mock_delete.assert_called_once_with(vars(test_args)['id'])
