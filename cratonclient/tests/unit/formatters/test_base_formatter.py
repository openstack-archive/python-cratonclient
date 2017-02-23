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
"""Tests for the base formatter class."""
import argparse

import mock

from cratonclient import crud
from cratonclient.formatters import base
from cratonclient.tests import base as testbase


class TestBaseFormatterInstantiation(testbase.TestCase):
    """Tests for cratonclient.formatters.base.Formatter creation."""

    def test_instantiation_calls_after_init(self):
        """Verify we call our postinitialization hook."""
        with mock.patch.object(base.Formatter, 'after_init') as after_init:
            base.Formatter(mock.Mock())

        after_init.assert_called_once_with()

    def test_stores_namespace_object(self):
        """Verify we store our parsed CLI arguments."""
        namespace = argparse.Namespace()
        formatter = base.Formatter(namespace)
        self.assertIs(namespace, formatter.args)


class TestBaseFormatter(testbase.TestCase):
    """Tests for cratonclient.formatters.base.Formatter behaviour."""

    def setUp(self):
        """Create test resources."""
        super(TestBaseFormatter, self).setUp()
        self.formatter = base.Formatter(argparse.Namespace())

    def test_handle_detects_resources(self):
        """Verify we handle instances explicitly."""
        resource = crud.Resource(mock.Mock(), {})
        method = 'handle_instance'
        with mock.patch.object(self.formatter, method) as handle_instance:
            self.formatter.handle(resource)

        handle_instance.assert_called_once_with(resource)

    def test_handle_detects_iterables(self):
        """Verify we handle generators explicitly."""
        method = 'handle_generator'
        iterable = iter([])
        with mock.patch.object(self.formatter, method) as handle_generator:
            self.formatter.handle(iterable)

        handle_generator.assert_called_once_with(iterable)
