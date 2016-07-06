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
from cratonclient.tests import base


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

    @mock.patch('cratonclient.shell.main.CratonShell.main')
    def test_main_catches_exception(self, cratonShellMainMock):
        """Verify exceptions will be caught and shell will exit properly."""
        cratonShellMainMock.side_effect = Exception(mock.Mock(status=404),
                                                    'some error')
        self.assertRaises(SystemExit, main.main)
