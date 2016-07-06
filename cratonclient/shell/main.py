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
import six
import sys

from oslo_utils import encodeutils


class CratonShell(object):
    """Class used to handle shell definition and parsing."""

    def get_base_parser(self):
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
                            action='store_true',
                            help=argparse.SUPPRESS)

        return parser

    def main(self, argv):
        """Main entry-point for cratonclient shell argument parsing."""
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        if options.help or not argv:
            parser.print_help()
            return 0


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
