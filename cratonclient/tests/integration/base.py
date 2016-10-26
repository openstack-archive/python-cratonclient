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
"""Some integration testing utilities."""

import mock
import six

from cratonclient.shell import main
from cratonclient.tests import base


class ShellTestCase(base.TestCase):
    """Test case base class for all shell unit tests."""

    def shell(self, arg_str, exitcodes=(0,)):
        """Main function for exercising the craton shell."""
        with mock.patch('sys.stdout', new=six.StringIO()) as mock_stdout, \
            mock.patch('sys.stderr', new=six.StringIO()) as mock_stderr:

            try:
                main_shell = main.CratonShell()
                main_shell.main(arg_str.split())
            except SystemExit:
                pass
            return (mock_stdout.getvalue(), mock_stderr.getvalue())
