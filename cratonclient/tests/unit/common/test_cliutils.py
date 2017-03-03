# -*- coding: utf-8 -*-

# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
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
"""Unit tests for the cratonclient.crud module members."""

import mock

from cratonclient.common import cliutils
from cratonclient.tests import base


class TestCLIUtils(base.TestCase):
    """Test for the CRUDClient class."""

    def test_convert_arg_value_bool(self):
        """Assert bool conversion."""
        trues = ['true', 'TRUE', 'True', 'trUE']
        falses = ['false', 'FALSE', 'False', 'falSe']

        for true in trues:
            self.assertTrue(cliutils.convert_arg_value(true))

        for false in falses:
            self.assertFalse(cliutils.convert_arg_value(false))

    def test_convert_arg_value_none(self):
        """Assert None conversion."""
        nones = ['none', 'null', 'NULL', 'None', 'NONE']

        for none in nones:
            self.assertIsNone(cliutils.convert_arg_value(none))

    def test_convert_arg_value_integer(self):
        """Assert integer conversion."""
        ints = ['1', '10', '145']

        for integer in ints:
            value = cliutils.convert_arg_value(integer)
            self.assertTrue(isinstance(value, int))

    def test_convert_arg_value_float(self):
        """Assert float conversion."""
        floats = ['5.234', '1.000', '1.0001', '224.1234']

        for num in floats:
            value = cliutils.convert_arg_value(num)
            self.assertTrue(isinstance(value, float))

    def test_convert_arg_value_string(self):
        """Assert string conversion."""
        strings = ["hello", "path/to/thing", "sp#cial!", "heyy:this:works"]

        for string in strings:
            value = cliutils.convert_arg_value(string)
            self.assertTrue(isinstance(value, str))

    def test_convert_arg_value_escapes(self):
        """Assert escaped conversion works to afford literal values."""
        escapes = ['"007"', '"1"', '"1.0"', '"False"', '"True"', '"None"']

        for escaped in escapes:
            value = cliutils.convert_arg_value(escaped)
            self.assertTrue(isinstance(value, str))

    @mock.patch('cratonclient.common.cliutils.sys.stdin')
    def test_variable_updates_from_args(self, mock_stdin):
        """Assert cliutils.variable_updates(...) when using arguments."""
        test_data = ["foo=bar", "test=", "baz=1", "bumbleywump=cucumberpatch"]
        mock_stdin.isatty.return_value = True
        expected_updates = {
            "foo": "bar",
            "baz": 1,
            "bumbleywump": "cucumberpatch"
        }
        expected_deletes = ["test"]

        updates, deletes = cliutils.variable_updates(test_data)

        self.assertEqual(expected_updates, updates)
        self.assertEqual(expected_deletes, deletes)

    @mock.patch('cratonclient.common.cliutils.sys.stdin')
    def test_variable_updates_from_stdin(self, mock_stdin):
        """Assert cliutils.variable_updates(...) when using stdin."""
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = \
            '{"foo": {"bar": "baz"}, "bumbleywump": "cucumberpatch"}'
        expected_updates = {
            "foo": {
                "bar": "baz"
            },
            "bumbleywump": "cucumberpatch"
        }

        updates, deletes = cliutils.variable_updates([])

        self.assertEqual(expected_updates, updates)
        self.assertEqual([], deletes)

    @mock.patch('cratonclient.common.cliutils.sys.stdin')
    def test_variable_deletes_from_args(self, mock_stdin):
        """Assert cliutils.variable_deletes(...) when using arguments."""
        test_data = ["foo", "test", "baz"]
        mock_stdin.isatty.return_value = True
        expected_deletes = test_data

        deletes = cliutils.variable_deletes(test_data)

        self.assertEqual(expected_deletes, deletes)

    @mock.patch('cratonclient.common.cliutils.sys.stdin')
    def test_variable_deletes_from_stdin(self, mock_stdin):
        """Assert cliutils.variable_deletes(...) when using stdin."""
        mock_stdin.isatty.return_value = False
        mock_stdin.read.return_value = \
            '["foo", "test", "baz"]'
        expected_deletes = ["foo", "test", "baz"]

        deletes = cliutils.variable_deletes([])

        self.assertEqual(expected_deletes, deletes)
