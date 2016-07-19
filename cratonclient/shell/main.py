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
"""Main shell for parsing arguments directed toward Craton."""

from __future__ import print_function

import argparse
import pkg_resources
import six
import sys

from oslo_utils import encodeutils

from cratonclient import __version__
from cratonclient.v1 import client


class CratonShell(object):
    """Class used to handle shell definition and parsing."""

    def get_base_parser(self, reg_cmd):
        """Configure base craton arguments and parsing."""
        parser = argparse.ArgumentParser(
            prog='craton',
            description=__doc__.strip(),
            epilog='See "craton help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=argparse.HelpFormatter
        )

        parser.add_argument('-h', '--help',
                            action='help',
                            help=argparse.SUPPRESS,
                            )
        parser.add_argument('--version',
                            action='version',
                            version=__version__,
                            )
        parser.add_argument('command',
                            choices=reg_cmd.keys(),
                            )
        parser.add_argument('args',
                            help=argparse.SUPPRESS,
                            nargs=argparse.REMAINDER,
                            )
        return parser

    def _registered_commands(self, shell_entry='registered_shell_versions'):
        """Find shell entry points for each version of the API."""
        reg_versions = pkg_resources.iter_entry_points(group=shell_entry)
        for ver in reg_versions:
            shell_main = ver.load()
            return {ver.name: shell_main()}

    def main(self, argv):
        """Main entry-point for cratonclient shell argument parsing."""
        # TODO(cmspence): Determine version/microversion programmatically
        #  We want to move towards microversioning like other projects
        cli_ver = 'v1'
        registered_commands = self._registered_commands()[cli_ver]
        parser = self.get_base_parser(registered_commands)
        if not argv:
            parser.print_help()
            return 0
        args = parser.parse_args(argv)
        reg = registered_commands[args.command]
        sub_cmd = reg.load()
        # TODO(cmspence): setup the client.
        # self.cs = client.Client(session,craton_service_url)
        self.cc = client.Client(None, "0.0.0.0")
        sub_cmd(self.cc, args.args)


def main():
    """Main entry-point for cratonclient's CLI."""
    try:
        CratonShell().main(map(encodeutils.safe_decode, sys.argv[1:]))
    except Exception as e:
        print("ERROR: %s" % encodeutils.safe_encode(six.text_type(e)),
              file=sys.stderr)
        sys.exit(1)

    return 0


if __name__ == "__main__":
    main()
