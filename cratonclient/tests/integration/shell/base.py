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
from cratonclient.v1 import variables


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
        self.resources = '{}s'.format(self.resource)
        self.resource_url = 'http://127.0.0.1/v1/{}/{}' \
            .format(self.resources, self.resource_id)
        self.variables_url = '{}/variables'.format(self.resource_url)
        self.test_args = Namespace(id=self.resource_id, formatter=mock.Mock())

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

        # NOTE(thomasem): Mock out a client to assert craton Python API calls
        self.client = mock.Mock()
        mock_resource = \
            getattr(self.client, self.resources).get.return_value
        mock_resource.variables = variables.VariableManager(
            self.mock_session, self.resource_url
        )

    def tearDown(self):
        """Clean up between tests."""
        super(VariablesTestCase, self).tearDown()
        self.stdin_patcher.stop()

    def _get_shell_func_for(self, suffix):
        return getattr(
            self.shell,
            'do_{}_vars_{}'.format(self.resource, suffix)
        )

    def test_do_vars_get_gets_correct_resource(self):
        """Assert the proper resource is retrieved when calling get."""
        self.mock_get_response.json.return_value = \
            {"variables": {"foo": "bar"}}
        self._get_shell_func_for('get')(self.client, self.test_args)
        getattr(self.client, self.resources).get.assert_called_once_with(
            vars(self.test_args)['id'])

    def test_do_vars_delete_gets_correct_resource(self):
        """Assert the proper resource is retrieved when calling delete."""
        self.test_args.variables = ['foo', 'bar']
        self._get_shell_func_for('delete')(self.client, self.test_args)
        getattr(self.client, self.resources).get.assert_called_once_with(
            vars(self.test_args)['id'])

    def test_do_vars_update_gets_correct_resource(self):
        """Assert the proper resource is retrieved when calling update."""
        self.test_args.variables = ['foo=', 'bar=']
        mock_resp_json = {"variables": {"foo": "bar"}}
        self.mock_get_response.json.return_value = mock_resp_json
        self.mock_put_response.json.return_value = mock_resp_json

        self._get_shell_func_for('set')(self.client, self.test_args)
        getattr(self.client, self.resources).get.assert_called_once_with(
            vars(self.test_args)['id'])

    def test_do_vars_get_calls_session_get(self):
        """Assert the proper resource is retrieved when calling get."""
        self.mock_get_response.json.return_value = \
            {"variables": {"foo": "bar"}}
        self._get_shell_func_for('get')(self.client, self.test_args)
        self.mock_session.get.assert_called_once_with(self.variables_url)

    def test_do_vars_delete_calls_session_delete(self):
        """Verify that <resource>-vars-delete calls expected session.delete."""
        self.test_args.variables = ['foo', 'bar']
        self._get_shell_func_for('delete')(self.client, self.test_args)
        self.mock_session.delete.assert_called_once_with(
            self.variables_url,
            json=('foo', 'bar'),
            params={},
        )

    def test_do_vars_update_calls_session_put(self):
        """Verify that <resource>-vars-delete calls expected session.delete."""
        self.test_args.variables = ['foo=baz', 'bar=boo', 'test=']
        mock_resp_json = {"variables": {"foo": "bar"}}
        self.mock_get_response.json.return_value = mock_resp_json
        self.mock_put_response.json.return_value = mock_resp_json

        self._get_shell_func_for('set')(self.client, self.test_args)
        self.mock_session.delete.assert_called_once_with(
            self.variables_url,
            json=('test',),
            params={},
        )
        self.mock_session.put.assert_called_once_with(
            self.variables_url,
            json={'foo': 'baz', 'bar': 'boo'}
        )
