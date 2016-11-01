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
        return argparse.Namespace(**kwargs)


class TestShellCommandUsingPrintDict(TestShellCommand):
    """Base class for shell commands using print_dict."""

    def setUp(self):
        """Initialize test fixtures."""
        super(TestShellCommandUsingPrintDict, self).setUp()
        self.print_dict_patch = mock.patch(
            'cratonclient.common.cliutils.print_dict'
        )
        self.print_dict = self.print_dict_patch.start()

    def tearDown(self):
        """Clean-up test fixtures."""
        super(TestShellCommandUsingPrintDict, self).tearDown()
        self.print_dict_patch.stop()

    def assertNothingWasCalled(self):
        """Assert inventory, list, and print_dict were not called."""
        self.assertFalse(self.craton_client.inventory.called)
        self.assertFalse(self.print_dict.called)


class TestShellCommandUsingPrintList(TestShellCommand):
    """Base class for shell commands using print_list."""

    def setUp(self):
        """Initialize test fixtures."""
        super(TestShellCommandUsingPrintList, self).setUp()
        self.print_list_patch = mock.patch(
            'cratonclient.common.cliutils.print_list'
        )
        self.print_list = self.print_list_patch.start()

    def tearDown(self):
        """Clean-up test fixtures."""
        super(TestShellCommandUsingPrintList, self).tearDown()
        self.print_list_patch.stop()

    def assertNothingWasCalled(self):
        """Assert inventory, list, and print_dict were not called."""
        self.assertFalse(self.craton_client.inventory.called)
        self.assertFalse(self.print_list.called)

    def assertSortedPrintListFieldsEqualTo(self, expected_fields):
        """Assert the sorted fields parameter is equal expected_fields."""
        self.assertEqual(expected_fields,
                         sorted(self.print_list.call_args[0][-1]))
