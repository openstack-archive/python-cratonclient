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
"""Unit tests for cratonclient.exceptions."""

from cratonclient import exceptions as exc
from cratonclient.tests import base

import mock


class TestExceptions(base.TestCase):
    """Tests for our exception handling convenience functions."""

    client_error_statuses = [
        400, 401, 403, 404, 405, 406, 407, 409, 410, 411, 412, 413, 414, 415,
        416, 422,
    ]

    server_error_statuses = [
        500,
    ]

    def mock_keystoneauth_exception_from(self, status_code):
        """Create a fake keystoneauth1 exception with a response attribute."""
        exception = mock.Mock()
        exception.response = self.mock_response_from(status_code)
        exception.http_status = status_code
        return exception

    def mock_response_from(self, status_code):
        """Create a mock requests.Response object."""
        response = mock.Mock()
        response.status_code = status_code
        return response

    def test_error_from_4xx(self):
        """Verify error_from's behvaiour for 4xx status codes."""
        for status in self.client_error_statuses:
            response = self.mock_response_from(status)
            self.assertIsInstance(exc.error_from(response),
                                  exc.HTTPClientError)

    def test_error_from_5xx(self):
        """Verify error_from's behvaiour for 5xx status codes."""
        for status in self.server_error_statuses:
            response = self.mock_response_from(status)
            self.assertIsInstance(exc.error_from(response),
                                  exc.HTTPServerError)

    def test_raise_from(self):
        """Verify raise_from handles keystoneauth1 exceptions."""
        for status in (self.client_error_statuses +
                       self.server_error_statuses):
            ksaexception = self.mock_keystoneauth_exception_from(status)
            exception = exc.raise_from(ksaexception)
            self.assertIs(ksaexception, exception.original_exception)
