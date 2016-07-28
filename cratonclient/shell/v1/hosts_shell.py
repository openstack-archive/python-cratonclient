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
"""Hosts resource and resource shell wrapper."""
from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1.hosts import HOST_FIELDS as h_fields


@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              type=int,
              help='Integer ID of the cell that contains '
                   'the desired list of hosts.')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Show detailed information about the hosts.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of hosts to return.')
@cliutils.arg('--sort-key',
              metavar='<field>',
              help='Host field that will be used for sorting.')
@cliutils.arg('--sort-dir',
              metavar='<direction>',
              default='asc',
              help='Sort direction: "asc" (default) or "desc".')
@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=[],
              help='Comma-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'Can not be used when "--detail" is specified')
def do_host_list(cc, args):
    """Print list of hosts which are registered with the Craton service."""
    params = {}
    default_fields = ['id', 'name', 'type', 'active', 'cell_id']
    if args.cell is not None:
        params['cell'] = args.cell
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit
    if args.detail:
        fields = h_fields
        params['detail'] = args.detail
    elif args.fields:
        fields = {x: h_fields[x] for x in args.fields}
    else:
        fields = {x: h_fields[x] for x in default_fields}
    if args.sort_key is not None:
        fields_map = dict(zip(fields.keys(), fields.keys()))
        # TODO(cmspence): Do we want to allow sorting by field heading value?
        try:
            sort_key = fields_map[args.sort_key]
        except KeyError:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(args.sort_key, h_fields.keys())
            )
        params['sort_key'] = sort_key
        if args.sort_dir is not None:
            if args.sort_dir not in ('asc', 'desc'):
                raise exc.CommandError('Invalid sort direction specified. The '
                                       'expected valid values for --sort-dir '
                                       'are: "asc", "desc".')
        params['sort_dir'] = args.sort_dir

    hosts = cc.hosts.list(args.craton_project_id, **params)
    cliutils.print_list(hosts, list(fields))
