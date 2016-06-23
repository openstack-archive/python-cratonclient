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

"""Tests for `cratonclient.shell.main` module."""

from cratonclient.shell import main
from cratonclient.tests import base


class TestMainShell(base.TestCase):
    """Test our craton main shell."""

    def test_main_returns_successfully(self):
        """Verify that cratonclient shell main returns as expected."""
        self.assertEqual(main.main(), 0)
