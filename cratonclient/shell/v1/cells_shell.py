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
"""Cells resource and resource shell wrapper."""
from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1.cells import CELL_FIELDS as c_fields


@cliutils.arg('region',
              metavar='<region>',
              type=int,
              help='ID of the region that the cell belongs to.')
@cliutils.arg('id',
              metavar='<cell>',
              type=int,
              help='ID of the cell.')
def do_cell_show(cc, args):
    """Show detailed information about a cell."""
    cell = cc.inventory(args.region).cells.get(args.id)
    data = {f: getattr(cell, f, '') for f in c_fields}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('-r', '--region',
              metavar='<region>',
              type=int,
              required=True,
              help='ID of the region that the cell belongs to.')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Show detailed information about the cells.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of cells to return.')
@cliutils.arg('--sort-key',
              metavar='<field>',
              help='Cell field that will be used for sorting.')
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
def do_cell_list(cc, args):
    """Print list of cells which are registered with the Craton service."""
    params = {}
    default_fields = ['id', 'name']
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit
    if args.detail:
        fields = c_fields
        params['detail'] = args.detail
    elif args.fields:
        fields = {x: c_fields[x] for x in args.fields}
    else:
        fields = {x: c_fields[x] for x in default_fields}
    if args.sort_key is not None:
        fields_map = dict(zip(fields.keys(), fields.keys()))
        # TODO(cmspence): Do we want to allow sorting by field heading value?
        try:
            sort_key = fields_map[args.sort_key]
        except KeyError:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(args.sort_key, c_fields.keys())
            )
        params['sort_key'] = sort_key
        if args.sort_dir is not None:
            if args.sort_dir not in ('asc', 'desc'):
                raise exc.CommandError('Invalid sort direction specified. The '
                                       'expected valid values for --sort-dir '
                                       'are: "asc", "desc".')
        params['sort_dir'] = args.sort_dir

    cells = cc.inventory(args.region).cells.list(**params)
    cliutils.print_list(cells, list(fields))


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the cell.')
@cliutils.arg('-p', '--project',
              dest='project_id',
              metavar='<project>',
              type=int,
              required=True,
              help='ID of the project that the cell belongs to.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              required=True,
              help='ID of the region that the cell belongs to.')
@cliutils.arg('--note',
              help='Note about the cell.')
def do_cell_create(cc, args):
    """Register a new cell with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in c_fields and not (v is None)}
    cell = cc.inventory(args.region_id).cells.create(**fields)
    data = {f: getattr(cell, f, '') for f in c_fields}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('region',
              metavar='<region>',
              type=int,
              help='Current ID of the region that the cell belongs to.')
@cliutils.arg('id',
              metavar='<cell>',
              type=int,
              help='ID of the cell.')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the cell.')
@cliutils.arg('-p', '--project',
              dest='project_id',
              metavar='<project>',
              type=int,
              required=True,
              help='Desired ID of the project that the cell should change to.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              required=True,
              help='Desired ID of the region that the cell should change to.')
@cliutils.arg('--note',
              help='Note about the cell.')
def do_cell_update(cc, args):
    """Update a cell that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in c_fields and not (v is None)}
    cell = cc.inventory(args.region).cells.update(**fields)
    data = {f: getattr(cell, f, '') for f in c_fields}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('region',
              metavar='<region>',
              type=int,
              help='ID of the region that the cell belongs to.')
@cliutils.arg('id',
              metavar='<cell>',
              type=int,
              help='ID of the cell.')
def do_cell_delete(cc, args):
    """Delete a cell that is registered with the Craton service."""
    response = cc.inventory(args.region).cells.delete(args.id)
    print("Cell {0} was {1}successfully deleted.".
          format(args.id, '' if response else 'un'))
