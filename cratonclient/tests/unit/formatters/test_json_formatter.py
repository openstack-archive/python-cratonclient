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
"""JSON formatter unit tests."""
import argparse
import json

import mock
import six

from cratonclient import crud
from cratonclient.formatters import json_format
from cratonclient.tests import base


class TestValidFormatting(base.TestCase):
    def args_for(self, **kwargs):
        """Return an instantiated argparse Namsepace.

        Using the specified keyword arguments, create and return a Namespace
        object from argparse for testing purposes.
        :returns:
            Instantiated namespace.
        :rtype:
            argparse.Namespace
        """
        return argparse.Namespace(**kwargs)

    def resource_info(self, **kwargs):
        """Return a dictionary with resource information.

        :returns:
            Dictionary with basic id and name as well as the provided keyword
            arguments.
        :rtype:
            dict
        """
        info = {
            'id': 1,
            'name': 'Test Resource',
        }
        info.update(kwargs)
        return info

    def stripped_stdout(self):
        """Return the newline stripped standard-out captured string."""
        stdout = self.stdout.getvalue().rstrip('\n')
        self.stdout_patcher.stop()
        return stdout

    def setUp(self):
        """Initialize our instance prior to each test."""
        super(TestValidFormatting, self).setUp()
        self.formatter = json_format.Formatter(self.args_for())
        self.stdout_patcher = mock.patch('sys.stdout', new=six.StringIO())
        self.stdout = self.stdout_patcher.start()

    def load_json(self, stdout):
        try:
            return json.loads(stdout)
        except ValueError as err:
            self.fail('Encountered a ValueError: %s' % err)

    def test_instance_handling_creates_valid_json(self):
        """Verify the printed data is valid JSON."""
        info = self.resource_info()
        instance = crud.Resource(mock.Mock(), info, loaded=True)
        self.formatter.handle(instance)
        parsed = self.load_json(self.stripped_stdout())
        self.assertDictEqual(info, parsed)

    def test_empty_generator_handling(self):
        """Verify we simply print an empty list."""
        self.formatter.handle(iter([]))
        parsed = self.load_json(self.stripped_stdout())
        self.assertEqual([], parsed)

    def test_generator_of_a_single_resource(self):
        """Verify we print the single list appropriately."""
        info = self.resource_info()
        self.formatter.handle(iter([crud.Resource(mock.Mock(), info, True)]))
        parsed = self.load_json(self.stripped_stdout())
        self.assertListEqual([info], parsed)

    def test_generator_of_more_than_one_resouurce(self):
        """Verify we handle multiple items in a generator correctly."""
        info_dicts = [self.resource_info(id=i) for i in range(10)]
        self.formatter.handle(crud.Resource(mock.Mock(), info, True)
                              for info in info_dicts)
        parsed = self.load_json(self.stripped_stdout())
        self.assertListEqual(info_dicts, parsed)
