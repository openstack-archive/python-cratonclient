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

"""Tests for `cratonclient.shell.main` module."""


import mock
import re

from testtools import matchers

from cratonclient.shell import main
from cratonclient.tests.integration import base


class TestMainShell(base.ShellTestCase):
    """Test our craton main shell."""

    re_options = re.DOTALL | re.MULTILINE

    @mock.patch('cratonclient.shell.main.CratonShell.main')
    def test_main_returns_successfully(self, cratonShellMainMock):
        """Verify that main returns as expected."""
        cratonShellMainMock.return_value = 0
        self.assertEqual(main.main(), 0)

    def test_print_help_no_args(self):
        """Verify that no arguments prints out help by default."""
        required_help_responses = [
            '.*?^usage: craton',
            '.*?^See "craton help COMMAND" '
            'for help on a specific command.',
        ]
        stdout, stderr = self.shell('')
        for r in required_help_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    def test_print_help_with_args(self):
        """Verify that help command(s) prints out help text correctly."""
        required_help_responses = [
            '.*?^usage: craton',
            '.*?^See "craton help COMMAND" '
            'for help on a specific command.',
        ]
        for help_args in ['-h', '--help']:
            stdout, stderr = self.shell(help_args)
            for r in required_help_responses:
                self.assertThat((stdout + stderr),
                                matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.client.Client')
    def test_main_craton_url(self, mock_client):
        """Verify that craton-url command is used for client connection."""
        self.shell('--craton-url http://localhost:9999/ host-list -r 1')
        mock_client.assert_called_with(mock.ANY, 'http://localhost:9999/')

    @mock.patch('cratonclient.session.Session')
    @mock.patch('cratonclient.v1.client.Client')
    def test_main_craton_project_id(self, mock_client, mock_session):
        """Verify --os-project-id command is used for client connection."""
        self.shell('--os-project-id 99 host-list -r 1')
        mock_session.assert_called_with(username=mock.ANY,
                                        token=mock.ANY,
                                        project_id='99')
        mock_client.assert_called_with(mock.ANY, mock.ANY)

    @mock.patch('cratonclient.session.Session')
    @mock.patch('cratonclient.v1.client.Client')
    def test_main_os_username(self, mock_client, mock_session):
        """Verify --os-username command is used for client connection."""
        self.shell('--os-username test host-list -r 1')
        mock_session.assert_called_with(username='test',
                                        token=mock.ANY,
                                        project_id=mock.ANY)
        mock_client.assert_called_with(mock.ANY, mock.ANY)

    @mock.patch('cratonclient.session.Session')
    @mock.patch('cratonclient.v1.client.Client')
    def test_main_os_password(self, mock_client, mock_session):
        """Verify --os-password command is used for client connection."""
        self.shell('--os-password test host-list -r 1')
        mock_session.assert_called_with(username=mock.ANY,
                                        token='test',
                                        project_id=mock.ANY)

        mock_client.assert_called_with(mock.ANY, mock.ANY)

    @mock.patch('cratonclient.shell.main.CratonShell.main')
    def test_main_catches_exception(self, cratonShellMainMock):
        """Verify exceptions will be caught and shell will exit properly."""
        cratonShellMainMock.side_effect = Exception(mock.Mock(status=404),
                                                    'some error')
        self.assertRaises(SystemExit, main.main)

    @mock.patch('cratonclient.shell.v1.hosts_shell.do_host_create')
    def test_main_routes_sub_command(self, mock_create):
        """Verify main shell calls correct subcommand."""
        url = '--craton-url test_url'
        username = '--os-username test_name'
        pw = '--os-password test_pw'
        proj_id = '--os-project-id 1'
        self.shell('{} {} {} {} host-create'.format(url,
                                                    username,
                                                    pw,
                                                    proj_id))

        self.assertTrue(mock_create.called)
