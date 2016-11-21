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
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import cells


@cliutils.arg('id',
              metavar='<cell>',
              type=int,
              help='ID of the cell.')
def do_cell_show(cc, args):
    """Show detailed information about a cell."""
    cell = cc.cells.get(args.id)
    data = {f: getattr(cell, f, '') for f in cells.CELL_FIELDS}
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
              choices=('asc', 'desc'),
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

    if args.fields and args.detail:
        raise exc.CommandError('Cannot specify both --fields and --detail.')

    if args.detail:
        fields = cells.CELL_FIELDS
        params['detail'] = args.detail
    elif args.fields:
        try:
            fields = {x: cells.CELL_FIELDS[x] for x in args.fields}
        except KeyError as keyerr:
            raise exc.CommandError('Invalid field "{}"'.format(keyerr.args[0]))
    else:
        fields = {x: cells.CELL_FIELDS[x] for x in default_fields}
    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in cells.CELL_FIELDS:
            raise exc.CommandError(
                ('"--sort-key" value was "{}" but should '
                 'be one of: {}').format(
                     args.sort_key,
                     ', '.join(cells.CELL_FIELDS.keys())
                )
            )
        params['sort_key'] = sort_key
    params['sort_dir'] = args.sort_dir
    params['region_id'] = args.region

    listed_cells = cc.cells.list(**params)
    cliutils.print_list(listed_cells, list(fields))


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the cell.')
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
              if k in cells.CELL_FIELDS and not (v is None)}
    cell = cc.cells.create(**fields)
    data = {f: getattr(cell, f, '') for f in cells.CELL_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<cell>',
              type=int,
              help='ID of the cell.')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the cell.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              help='Desired ID of the region that the cell should change to.')
@cliutils.arg('--note',
              help='Note about the cell.')
def do_cell_update(cc, args):
    """Update a cell that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in cells.CELL_FIELDS and not (v is None)}
    cell_id = fields.pop('id')
    if not fields:
        raise exc.CommandError(
            'Nothing to update... Please specify one of --name, --region, '
            'or --note'
        )
    cell = cc.cells.update(cell_id, **fields)
    data = {f: getattr(cell, f, '') for f in cells.CELL_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<cell>',
              type=int,
              help='ID of the cell.')
def do_cell_delete(cc, args):
    """Delete a cell that is registered with the Craton service."""
    try:
        response = cc.cells.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete cell {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc)
            )
        )
    else:
        print("Cell {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
