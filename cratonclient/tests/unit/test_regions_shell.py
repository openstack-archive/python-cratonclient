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
from cratonclient.tests import base
from cratonclient.v1 import regions


class TestRegionsShell(base.ShellTestCase):
    """Test craton regions shell commands."""

    re_options = re.DOTALL | re.MULTILINE
    region_valid_fields = None
    region_invalid_field = None

    def setUp(self):
        """Setup required test fixtures."""
        super(TestRegionsShell, self).setUp()
        self.region_valid_fields = Namespace(project_id=1,
                                             id=1,
                                             name='mock_region')
        self.region_invalid_field = Namespace(project_id=1,
                                              id=1,
                                              name='mock_region',
                                              invalid_foo='ignored')

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
        mock_create.assert_called_once_with(**vars(self.region_valid_fields))

    @mock.patch('cratonclient.v1.regions.RegionManager.create')
    def test_do_region_create_ignores_unknown_fields(self, mock_create):
        """Verify that do region create ignores unknown field."""
        client = mock.Mock()
        session = mock.Mock()
        session.project_id = 1
        client.regions = regions.RegionManager(session, 'http://127.0.0.1/')
        regions_shell.do_region_create(client, self.region_invalid_field)
        mock_create.assert_called_once_with(**vars(self.region_valid_fields))

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
        test_args = Namespace(id=1)
        regions_shell.do_region_show(client, test_args)
        mock_get.assert_called_once_with(vars(test_args)['id'])

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
