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
"""Base TestCase class for Formatter tests."""
import argparse

import mock
import six

from cratonclient.tests import base


class FormatterTestCase(base.TestCase):
    """Base-level Formatter TestCase class."""

    def patch_stdout(self, autostart=True):
        """Patch sys.stdout and capture all output to it.

        This will automatically start the patch by default.

        :param bool autostart:
            Start patching sys.stdout immediately or delay that until later.
        """
        self.stdout_patcher = mock.patch('sys.stdout', new=six.StringIO())
        if autostart:
            self.stdout = self.stdout_patcher.start()
            self.addCleanup(self.unpatch_stdout)

    def unpatch_stdout(self):
        if getattr(self.stdout_patcher, 'is_local', None) is not None:
            self.stdout_patcher.stop()

    def stripped_stdout(self):
        """Return the newline stripped standard-out captured string."""
        stdout = self.stdout.getvalue().rstrip('\n')
        self.unpatch_stdout()
        return stdout

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
