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

"""Tests for `cratonclient.shell.v1.hosts_shell` module."""

import mock

from cratonclient.tests import base


class TestHostsShell(base.ShellTestCase):
    """Test our craton hosts shell commands."""

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_success(self, mock_list):
        """Verify that no arguments prints out all project hosts."""
        self.shell('host-list')
        self.assertTrue(mock_list.called)
