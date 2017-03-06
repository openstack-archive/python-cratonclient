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
"""Resources for the shell integration tests."""

from argparse import Namespace
import mock
import six

from cratonclient.shell import main
from cratonclient.tests import base


class ShellTestCase(base.TestCase):
    """Test case base class for all shell unit tests."""

    def shell(self, arg_str, exitcodes=(0,)):
        """Main function for exercising the craton shell."""
        with mock.patch('sys.stdout', new=six.StringIO()) as mock_stdout, \
            mock.patch('sys.stderr', new=six.StringIO()) as mock_stderr:

            try:
                main_shell = main.CratonShell()
                main_shell.main(arg_str.split())
            except SystemExit:
                pass
            return (mock_stdout.getvalue(), mock_stderr.getvalue())


class VariablesTestCase(base.TestCase):
    """Test Host Variable shell calls."""

    def setUp(self):
        """Basic set up for all tests in this suite."""
        super(VariablesTestCase, self).setUp()
        self.resource_url = 'http://127.0.0.1/v1/hosts/1'
        self.variables_url = '{}/variables'.format(self.resource_url)
        self.test_args = Namespace(id=1, formatter=mock.Mock())

        # NOTE(thomasem): Make all calls seem like they come from CLI args
        self.stdin_patcher = \
            mock.patch('cratonclient.common.cliutils.sys.stdin')
        self.patched_stdin = self.stdin_patcher.start()
        self.patched_stdin.isatty.return_value = True

        # NOTE(thomasem): Mock out a session object to assert resulting API
        # calls
        self.mock_session = mock.Mock()
        self.mock_get_response = self.mock_session.get.return_value
        self.mock_put_response = self.mock_session.put.return_value
        self.mock_delete_response = self.mock_session.delete.return_value
        self.mock_delete_response.status_code = 204
