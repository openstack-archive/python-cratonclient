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
