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
import re

from testtools import matchers

from cratonclient.tests import base


class TestHostsShell(base.ShellTestCase):
    """Test our craton hosts shell commands."""

    re_options = re.DOTALL | re.MULTILINE

    @mock.patch('cratonclient.v1.hosts.HostManager.list')
    def test_host_list_success(self, mock_list):
        """Verify that no arguments prints out all project hosts."""
        self.shell('host-list')
        self.assertTrue(mock_list.called)

    def test_host_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-create',
            '.*?^craton host-create: error: argument -n/--name is required',
        ]
        stdout, stderr = self.shell('host-create')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.create')
    def test_host_create_success(self, mock_create):
        """Verify that all required create args results in success."""
        self.shell('host-create -p 1 -r 1 -n test -i 127.0.0.1')
        self.assertTrue(mock_create.called)

    def test_host_update_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-update',
            '.*?^craton host-update: error: too few arguments',
        ]
        stdout, stderr = self.shell('host-update')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.update')
    def test_host_update_success(self, mock_update):
        """Verify that all required update args results in success."""
        self.shell('host-update 1')
        self.assertTrue(mock_update.called)

    def test_host_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton host-show',
            '.*?^craton host-show: error: too few arguments',
        ]
        stdout, stderr = self.shell('host-show')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.hosts.HostManager.get')
    def test_host_show_success(self, mock_get):
        """Verify that all required update args results in success."""
        self.shell('host-show 1')
        self.assertTrue(mock_get.called)
