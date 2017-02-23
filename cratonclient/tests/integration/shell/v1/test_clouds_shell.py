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
"""Tests for `cratonclient.shell.v1.clouds_shell` module."""
import mock
import re

from argparse import Namespace
from testtools import matchers

from cratonclient.shell.v1 import clouds_shell
from cratonclient.tests.integration.shell import base
from cratonclient.v1 import clouds


class TestCloudsShell(base.ShellTestCase):
    """Test craton clouds shell commands."""

    re_options = re.DOTALL | re.MULTILINE
    cloud_valid_fields = None
    cloud_invalid_field = None

    def setUp(self):
        """Setup required test fixtures."""
        super(TestCloudsShell, self).setUp()
        self.cloud_valid_fields = Namespace(project_id=1,
                                            id=1,
                                            name='mock_cloud')
        self.cloud_invalid_field = Namespace(project_id=1,
                                             id=1,
                                             name='mock_cloud',
                                             invalid_foo='ignored')

    def test_cloud_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cloud-create',
            '.*?^craton cloud-create: error:.*$'
        ]
        stdout, stderr = self.shell('cloud-create')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.clouds.CloudManager.create')
    def test_do_cloud_create_calls_cloud_manager(self, mock_create):
        """Verify that do cloud create calls CloudManager create."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.clouds = clouds.CloudManager(session, 'http://127.0.0.1/')
        clouds_shell.do_cloud_create(client, self.cloud_valid_fields)
        mock_create.assert_called_once_with(**vars(self.cloud_valid_fields))

    @mock.patch('cratonclient.v1.clouds.CloudManager.create')
    def test_do_cloud_create_ignores_unknown_fields(self, mock_create):
        """Verify that do cloud create ignores unknown field."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.clouds = clouds.CloudManager(session, 'http://127.0.0.1/')
        clouds_shell.do_cloud_create(client, self.cloud_invalid_field)
        mock_create.assert_called_once_with(**vars(self.cloud_valid_fields))

    def test_cloud_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cloud-show',
            '.*?^craton cloud-show: error:.*$',
        ]
        stdout, stderr = self.shell('cloud-show')
        actual_output = stdout + stderr
        for r in expected_responses:
            self.assertThat(actual_output,
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.clouds.CloudManager.get')
    def test_do_cloud_show_calls_cloud_manager_with_fields(self, mock_get):
        """Verify that do cloud show calls CloudManager get."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.clouds = clouds.CloudManager(session, 'http://127.0.0.1/')
        test_args = Namespace(id=1)
        clouds_shell.do_cloud_show(client, test_args)
        mock_get.assert_called_once_with(vars(test_args)['id'])

    def test_cloud_delete_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cloud-delete',
            '.*?^craton cloud-delete: error:.*$',
        ]
        stdout, stderr = self.shell('cloud-delete')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.clouds.CloudManager.delete')
    def test_do_cloud_delete_calls_cloud_manager(self, mock_delete):
        """Verify that do cloud delete calls CloudManager delete."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.clouds = clouds.CloudManager(session, 'http://127.0.0.1/')
        test_args = Namespace(id=1)
        clouds_shell.do_cloud_delete(client, test_args)
        mock_delete.assert_called_once_with(vars(test_args)['id'])

    def test_cloud_update_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton cloud-update',
            '.*?^craton cloud-update: error:.*$',
        ]
        stdout, stderr = self.shell('cloud-update')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.clouds.CloudManager.update')
    def test_do_cloud_update_calls_cloud_manager(self, mock_update):
        """Verify that do cloud update calls CloudManager update."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.clouds = clouds.CloudManager(session, 'http://127.0.0.1/')
        valid_input = Namespace(id=1,
                                name='mock_cloud')
        clouds_shell.do_cloud_update(client, valid_input)
        mock_update.assert_called_once_with(1, name='mock_cloud')

    @mock.patch('cratonclient.v1.clouds.CloudManager.update')
    def test_do_cloud_update_ignores_unknown_fields(self, mock_update):
        """Verify that do cloud update ignores unknown field."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.clouds = clouds.CloudManager(session, 'http://127.0.0.1/')
        invalid_input = Namespace(id=1,
                                  name='mock_cloud',
                                  invalid=True)
        clouds_shell.do_cloud_update(client, invalid_input)
        mock_update.assert_called_once_with(1, name='mock_cloud')
