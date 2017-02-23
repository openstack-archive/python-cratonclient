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
import sys

from oslo_utils import encodeutils
from oslo_utils import importutils
from stevedore import extension

from cratonclient import __version__
from cratonclient import exceptions as exc
from cratonclient import session as craton

from cratonclient.common import cliutils
from cratonclient.v1 import client


FORMATTERS_NAMESPACE = 'cratonclient.formatters'


class CratonShell(object):
    """Class used to handle shell definition and parsing."""

    def __init__(self):
        self.extension_mgr = extension.ExtensionManager(
            namespace=FORMATTERS_NAMESPACE,
            invoke_on_load=False,
        )

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
                            help=argparse.SUPPRESS,
                            )
        parser.add_argument('--version',
                            action='version',
                            version=__version__,
                            )
        parser.add_argument('--format',
                            choices=list(self.extension_mgr.names()),
                            help='The format to use to print the information '
                                 'to the console. Defaults to pretty-printing '
                                 'using ASCII tables.',
                            )
        parser.add_argument('--craton-url',
                            default=cliutils.env('CRATON_URL'),
                            help='The base URL of the running Craton service.'
                                 ' Defaults to env[CRATON_URL].',
                            )
        parser.add_argument('--craton-version',
                            type=int,
                            default=cliutils.env('CRATON_VERSION',
                                                 default=1),
                            help='The version of the Craton API to use. '
                                 'Defaults to env[CRATON_VERSION].'
                            )
        parser.add_argument('--os-project-id',
                            default=cliutils.env('OS_PROJECT_ID'),
                            help='The project ID used to authenticate to '
                                 'Craton. Defaults to env[OS_PROJECT_ID].',
                            )
        parser.add_argument('--os-username',
                            default=cliutils.env('OS_USERNAME'),
                            help='The username used to authenticate to '
                                 'Craton. Defaults to env[OS_USERNAME].',
                            )
        parser.add_argument('--os-password',
                            default=cliutils.env('OS_PASSWORD'),
                            help='The password used to authenticate to '
                                 'Craton. Defaults to env[OS_PASSWORD].',
                            )
        return parser

    # NOTE(cmspence): Credit for this get_subcommand_parser function
    # goes to the magnumclient developers and contributors.
    def get_subcommand_parser(self, api_version):
        """Get subcommands by parsing COMMAND_MODULES."""
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>',
                                           dest='subparser_name')
        shell = importutils.import_versioned_module(
            'cratonclient.shell',
            api_version,
            'shell',
        )
        command_modules = shell.COMMAND_MODULES
        for command_module in command_modules:
            self._find_subparsers(subparsers, command_module)
        self._find_subparsers(subparsers, self)
        return parser

    # NOTE(cmspence): Credit for this function goes to the
    # magnumclient developers and contributors.
    def _find_subparsers(self, subparsers, actions_module):
        """Find subparsers by looking at *_shell files."""
        help_formatter = argparse.HelpFormatter
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip()
            arguments = getattr(callback, 'arguments', [])
            subparser = (subparsers.add_parser(command,
                                               help=action_help,
                                               description=desc,
                                               add_help=False,
                                               formatter_class=help_formatter)
                         )
            subparser.add_argument('-h', '--help',
                                   action='help',
                                   help=argparse.SUPPRESS)
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def main(self, argv):
        """Main entry-point for cratonclient shell argument parsing."""
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        subcommand_parser = (
            self.get_subcommand_parser(options.craton_version)
        )
        self.parser = subcommand_parser

        if options.help or not argv:
            self.parser.print_help()
            return 0

        args = subcommand_parser.parse_args(argv)

        # Short-circuit and deal with help right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0

        session = craton.Session(
            username=args.os_username,
            token=args.os_password,
            project_id=args.os_project_id,
        )
        self.cc = client.Client(session, args.craton_url)
        args.formatter = self.extension_mgr[args.format](args)
        args.func(self.cc, args)

    @cliutils.arg(
        'command',
        metavar='<subcommand>',
        nargs='?',
        help='Display help for <subcommand>.')
    def do_help(self, args):
        """Display help about this program or one of its subcommands."""
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()


def main():
    """Main entry-point for cratonclient's CLI."""
    try:
        CratonShell().main([encodeutils.safe_decode(a) for a in sys.argv[1:]])
    except Exception as e:
        print("ERROR: {}".format(encodeutils.exception_to_unicode(e)),
              file=sys.stderr)
        sys.exit(1)
    return 0


if __name__ == "__main__":
    main()
