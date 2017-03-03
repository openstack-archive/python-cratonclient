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
"""Tests for `cratonclient.v1.clouds` module."""

from cratonclient import crud
from cratonclient.tests import base
from cratonclient.v1 import variables

import mock


class TestVariables(base.TestCase):
    """Tests for the Cloud Resource."""

    def setUp(self):
        """Basic test setup."""
        super(TestVariables, self).setUp()
        session = mock.Mock()
        self.variable_mgr = variables.VariableManager(session, '')

    def test_is_a_crudclient(self):
        """Verify our CloudManager is a CRUDClient."""
        self.assertIsInstance(self.variable_mgr, crud.CRUDClient)

    def test_variables_dict(self):
        """Assert Variables instantiation produces sane variables dict."""
        test_data = {
            "foo": "bar",
            "zoo": {
                "baz": "boo"
            }
        }
        resource_obj = self.variable_mgr.resource_class(
            mock.Mock(),
            {"variables": test_data}
        )

        expected_variables_dict = {
            "foo": variables.Variable("foo", "bar"),
            "zoo": variables.Variable("zoo", {
                "baz": variables.Variable("baz", "boo")
                })
        }
        self.assertDictEqual(expected_variables_dict,
                             resource_obj._variables_dict)

    def test_to_dict(self):
        """Assert Variables.to_dict() produces original variables dict."""
        test_data = {
            "foo": "bar",
            "zoo": {
                "baz": "boo"
            }
        }
        resource_obj = self.variable_mgr.resource_class(
            mock.Mock(),
            {"variables": test_data}
        )

        self.assertDictEqual(test_data, resource_obj.to_dict())
