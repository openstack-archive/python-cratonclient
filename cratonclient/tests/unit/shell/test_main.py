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
"""Tests for the cratonclient.shell.main module."""
import argparse
import sys

import mock
import six

import cratonclient
from cratonclient.shell import main
from cratonclient.tests import base


class TestEntryPoint(base.TestCase):
    """Tests for the craton shell entry-point."""

    def setUp(self):
        """Patch out the CratonShell class."""
        super(TestEntryPoint, self).setUp()
        self.class_mock = mock.patch('cratonclient.shell.main.CratonShell')
        self.craton_shell = self.class_mock.start()
        self.addCleanup(self.class_mock.stop)
        self.print_mock = mock.patch('cratonclient.shell.main.print')
        self.print_func = self.print_mock.start()
        self.addCleanup(self.print_mock.stop)
        self.sys_exit_mock = mock.patch('sys.exit')
        self.sys_exit = self.sys_exit_mock.start()
        self.addCleanup(self.sys_exit_mock.stop)

    def test_entry_point_creates_a_shell_instance(self):
        """Verify that our main entry-point uses CratonShell."""
        CratonShell = self.craton_shell

        main.main()

        CratonShell.assert_called_once_with()

    def test_entry_point_calls_shell_main_method(self):
        """Verify we call the main method on our CratonShell instance."""
        shell_instance = mock.Mock()
        self.craton_shell.return_value = shell_instance

        main.main()

        self.assertTrue(shell_instance.main.called)

    def test_entry_point_converts_args_to_text(self):
        """Verify we call the main method with a list of text objects."""
        shell_instance = mock.Mock()
        self.craton_shell.return_value = shell_instance

        main.main()

        # NOTE(sigmavirus24): call_args is a tuple of positional arguments and
        # keyword arguments, so since we pass a list positionally, we want the
        # first of the positional arguments.
        arglist = shell_instance.main.call_args[0][0]
        self.assertTrue(
            all(isinstance(arg, six.text_type) for arg in arglist)
        )

    def test_entry_point_handles_all_exceptions(self):
        """Verify that we handle unexpected exceptions and print a message."""
        shell_instance = mock.Mock()
        shell_instance.main.side_effect = ValueError
        self.craton_shell.return_value = shell_instance

        main.main()

        self.print_func.assert_called_once_with(
            "ERROR: ",
            file=sys.stderr,
        )


class TestCratonShell(base.TestCase):
    """Tests for the CratonShell class."""

    def setUp(self):
        """Create an instance of CratonShell for each test."""
        super(TestCratonShell, self).setUp()
        self.shell = main.CratonShell()

    def test_get_base_parser(self):
        """Verify how we construct our basic Argument Parser."""
        with mock.patch('argparse.ArgumentParser') as ArgumentParser:
            parser = self.shell.get_base_parser()

        self.assertEqual(ArgumentParser.return_value, parser)
        ArgumentParser.assert_called_once_with(
            prog='craton',
            description=('Main shell for parsing arguments directed toward '
                         'Craton.'),
            epilog='See "craton help COMMAND" for help on a specific command.',
            add_help=False,
            formatter_class=argparse.HelpFormatter,
        )

    def test_get_base_parser_sets_default_options(self):
        """Verify how we construct our basic Argument Parser."""
        with mock.patch('cratonclient.common.cliutils.env') as env:
            env.return_value = ''
            with mock.patch('argparse.ArgumentParser'):
                parser = self.shell.get_base_parser()

        self.assertEqual([
            mock.call(
                '-h', '--help', action='store_true', help=argparse.SUPPRESS,
            ),
            mock.call(
                '--version', action='version',
                version=cratonclient.__version__,
            ),
            mock.call(
                '--craton-url', default='',
                help='The base URL of the running Craton service. '
                     'Defaults to env[CRATON_URL].',
            ),
            mock.call(
                '--craton-version', default='',
                type=int,
                help='The version of the Craton API to use. '
                     'Defaults to env[CRATON_VERSION].'
            ),
            mock.call(
                '--os-project-id', default='',
                help='The project ID used to authenticate to Craton. '
                     'Defaults to env[OS_PROJECT_ID].',
            ),
            mock.call(
                '--os-username', default='',
                help='The username used to authenticate to Craton. '
                     'Defaults to env[OS_USERNAME].',
            ),
            mock.call(
                '--os-password', default='',
                help='The password used to authenticate to Craton. '
                     'Defaults to env[OS_PASSWORD].',
            ),
            ],
            parser.add_argument.call_args_list,
        )

    def test_get_base_parser_retrieves_environment_values(self):
        """Verify the environment variables that are requested."""
        with mock.patch('cratonclient.common.cliutils.env') as env:
            self.shell.get_base_parser()

        self.assertEqual([
            mock.call('CRATON_URL'),
            mock.call('CRATON_VERSION', default=1),
            mock.call('OS_PROJECT_ID'),
            mock.call('OS_USERNAME'),
            mock.call('OS_PASSWORD'),
            ],
            env.call_args_list,
        )
