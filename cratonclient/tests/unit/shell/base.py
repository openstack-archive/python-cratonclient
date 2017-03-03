# -*- coding: utf-8 -*-

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
"""Base class for shell unit tests."""
import argparse

import mock

from cratonclient import exceptions
from cratonclient.tests import base


class TestShellCommand(base.TestCase):
    """Base class for shell command unit tests."""

    def setUp(self):
        """Initialize test fixtures."""
        super(TestShellCommand, self).setUp()
        self.formatter = mock.Mock()
        self.formatter.configure.return_value = self.formatter
        self.craton_client = mock.Mock()
        self.inventory = mock.Mock()
        self.craton_client.inventory.return_value = self.inventory

    def assertRaisesCommandErrorWith(self, func, args):
        """Assert the shell command raises CommandError."""
        self.assertRaises(
            exceptions.CommandError,
            func, self.craton_client, args,
        )

    def args_for(self, **kwargs):
        """Return a Namespace object with the specified kwargs."""
        kwargs.setdefault('formatter', self.formatter)
        return argparse.Namespace(**kwargs)

    def assertNothingWasCalled(self):
        """Assert nothing was called on the formatter."""
        self.assertListEqual([], self.craton_client.mock_calls)
        self.assertFalse(self.formatter.configure.called)
        self.assertFalse(self.formatter.handle.called)

    def assertFieldsEqualTo(self, expected_fields):
        """Assert the sorted fields parameter is equal expected_fields."""
        kwargs = self.formatter.configure.call_args[1]
        self.assertListEqual(expected_fields, kwargs['fields'])
