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

from testtools import matchers

from cratonclient.tests import base


class TestRegionsShell(base.ShellTestCase):
    """Test craton regions shell commands."""

    re_options = re.DOTALL | re.MULTILINE

    def test_region_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-create',
            '.*?^craton region-create: error:.*$'
        ]
        stdout, stderr = self.shell('region-create')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.create')
    def test_region_create_success(self, mock_create):
        """Verify that all required create args results in success."""
        self.shell('region-create -n region')
        self.assertTrue(mock_create.called)
