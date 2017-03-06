# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for `cratonclient.shell.v1.regions_shell` module."""
import mock
import re

from argparse import Namespace
from testtools import matchers

from cratonclient.shell.v1 import regions_shell
from cratonclient.tests.integration.shell import base
from cratonclient.v1 import regions
from cratonclient.v1 import variables


class TestRegionsShell(base.ShellTestCase):
    """Test craton regions shell commands."""

    re_options = re.DOTALL | re.MULTILINE
    region_valid_fields = None
    region_invalid_fields = None

    def setUp(self):
        """Setup required test fixtures."""
        super(TestRegionsShell, self).setUp()
        self.region_valid_kwargs = {
            'project_id': 1,
            'id': 1,
            'name': 'mock_region',
        }
        self.region_invalid_kwargs = {
            'project_id': 1,
            'id': 1,
            'name': 'mock_region',
            'invalid_foo': 'ignored',
        }
        self.region_valid_fields = Namespace(**self.region_valid_kwargs)
        self.region_invalid_fields = Namespace(**self.region_invalid_kwargs)
        self.region_valid_fields.formatter = mock.Mock()
        self.region_invalid_fields.formatter = mock.Mock()

    def test_region_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-create',
            '.*?^craton region-create: error:.*$'
        ]
        stdout, stderr = self.shell('region-create')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.create')
    def test_do_region_create_calls_region_manager(self, mock_create):
        """Verify that do region create calls RegionManager create."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        regions_shell.do_region_create(client, self.region_valid_fields)
        mock_create.assert_called_once_with(**self.region_valid_kwargs)

    @mock.patch('cratonclient.v1.regions.RegionManager.create')
    def test_do_region_create_ignores_unknown_fields(self, mock_create):
        """Verify that do region create ignores unknown field."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        regions_shell.do_region_create(client, self.region_invalid_fields)
        mock_create.assert_called_once_with(**self.region_valid_kwargs)

    def test_region_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-show',
            '.*?^craton region-show: error:.*$',
        ]
        stdout, stderr = self.shell('region-show')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.get')
    def test_do_region_show_calls_region_manager_with_fields(self, mock_get):
        """Verify that do region show calls RegionManager get."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        test_args = Namespace(id=1, formatter=mock.Mock())
        regions_shell.do_region_show(client, test_args)
        mock_get.assert_called_once_with(1)

    def test_region_delete_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-delete',
            '.*?^craton region-delete: error:.*$',
        ]
        stdout, stderr = self.shell('region-delete')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.delete')
    def test_do_region_delete_calls_region_manager(self, mock_delete):
        """Verify that do region delete calls RegionManager delete."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        test_args = Namespace(id=1)
        regions_shell.do_region_delete(client, test_args)
        mock_delete.assert_called_once_with(vars(test_args)['id'])

    def test_region_update_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-update',
            '.*?^craton region-update: error:.*$',
        ]
        stdout, stderr = self.shell('region-update')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.update')
    def test_do_region_update_calls_region_manager(self, mock_update):
        """Verify that do region update calls RegionManager update."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        valid_input = Namespace(id=1,
                                name='mock_region',
                                formatter=mock.Mock())
        regions_shell.do_region_update(client, valid_input)
        mock_update.assert_called_once_with(1, name='mock_region')

    @mock.patch('cratonclient.v1.regions.RegionManager.update')
    def test_do_region_update_ignores_unknown_fields(self, mock_update):
        """Verify that do region update ignores unknown field."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        invalid_input = Namespace(id=1,
                                  name='mock_region',
                                  invalid=True,
                                  formatter=mock.Mock())
        regions_shell.do_region_update(client, invalid_input)
        mock_update.assert_called_once_with(1, name='mock_region')

    @mock.patch('cratonclient.v1.regions.RegionManager.list')
    def test_region_list_with_vars_success(self, mock_list):
        """Verify --vars arguments successfully passed to Client."""
        self.shell('region-list --vars a:b')
        mock_list.assert_called_once_with(
            vars='a:b',
            marker=None,
            autopaginate=False,
        )
        mock_list.reset_mock()


class TestRegionsVarsShell(base.VariablesTestCase):
    """Test Region Variable shell calls."""

    def setUp(self):
        """Basic set up for all tests in this suite."""
        super(TestRegionsVarsShell, self).setUp()

        # NOTE(thomasem): Mock out a client to assert craton Python API calls
        self.client = mock.Mock()
        self.mock_region_resource = self.client.regions.get.return_value
        self.mock_region_resource.variables = variables.VariableManager(
            self.mock_session, self.resource_url
        )

    def tearDown(self):
        """Clean up between tests."""
        super(TestRegionsVarsShell, self).tearDown()
        self.stdin_patcher.stop()

    def test_do_region_vars_get_gets_correct_region(self):
        """Assert the proper region is retrieved when calling get."""
        self.mock_get_response.json.return_value = \
            {"variables": {"foo": "bar"}}
        regions_shell.do_region_vars_get(self.client, self.test_args)
        self.client.regions.get.assert_called_once_with(
            vars(self.test_args)['id'])

    def test_do_region_vars_delete_gets_correct_region(self):
        """Assert the proper region is retrieved when calling delete."""
        self.test_args.variables = ['foo', 'bar']
        regions_shell.do_region_vars_delete(self.client, self.test_args)
        self.client.regions.get.assert_called_once_with(
            vars(self.test_args)['id'])

    def test_do_region_vars_update_gets_correct_region(self):
        """Assert the proper region is retrieved when calling update."""
        self.test_args.variables = ['foo=', 'bar=']
        mock_resp_json = {"variables": {"foo": "bar"}}
        self.mock_get_response.json.return_value = mock_resp_json
        self.mock_put_response.json.return_value = mock_resp_json

        regions_shell.do_region_vars_set(self.client, self.test_args)
        self.client.regions.get.assert_called_once_with(
            vars(self.test_args)['id'])

    def test_do_region_vars_get_calls_session_get(self):
        """Assert the proper region is retrieved when calling get."""
        self.mock_get_response.json.return_value = \
            {"variables": {"foo": "bar"}}
        regions_shell.do_region_vars_get(self.client, self.test_args)
        self.mock_session.get.assert_called_once_with(self.variables_url)

    def test_do_region_vars_delete_calls_session_delete(self):
        """Verify that do region-vars-delete calls expected session.delete."""
        self.test_args.variables = ['foo', 'bar']
        regions_shell.do_region_vars_delete(self.client, self.test_args)
        self.mock_session.delete.assert_called_once_with(
            self.variables_url,
            json=('foo', 'bar'),
            params={},
        )

    def test_do_region_vars_update_calls_session_put(self):
        """Verify that do region-vars-delete calls expected session.delete."""
        self.test_args.variables = ['foo=baz', 'bar=boo', 'test=']
        mock_resp_json = {"variables": {"foo": "bar"}}
        self.mock_get_response.json.return_value = mock_resp_json
        self.mock_put_response.json.return_value = mock_resp_json

        regions_shell.do_region_vars_set(self.client, self.test_args)
        self.mock_session.delete.assert_called_once_with(
            self.variables_url,
            json=('test',),
            params={},
        )
        self.mock_session.put.assert_called_once_with(
            self.variables_url,
            json={'foo': 'baz', 'bar': 'boo'}
        )
