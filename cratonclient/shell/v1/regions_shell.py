# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Hosts resource and resource shell wrapper."""
from __future__ import print_function

import argparse

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import regions


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the region.')
@cliutils.arg('--note',
              help='Note about the region.')
def do_region_create(cc, args):
    """Register a new region with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in regions.REGION_FIELDS and not (v is None)}

    region = cc.regions.create(**fields)
    data = {f: getattr(region, f, '') for f in regions.REGION_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of regions to return.')
@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=[],
              help='Comma-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'Can not be used when "--detail" is specified')
def do_region_list(cc, args):
    """List all regions."""
    params = {}
    default_fields = ['id', 'name']
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit

    if args.fields:
        try:
            fields = {x: regions.REGION_FIELDS[x] for x in args.fields}
        except KeyError as err:
            raise exc.CommandError('Invalid field "{}"'.format(err.args[0]))
    else:
        fields = default_fields

    regions_list = cc.regions.list(**params)
    cliutils.print_list(regions_list, list(fields))


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region.')
def do_region_show(cc, args):
    """Show detailed information about a region."""
    region = cc.regions.get(args.id)
    data = {f: getattr(region, f, '') for f in regions.REGION_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the region.')
@cliutils.arg('--note',
              help='Note about the region.')
def do_region_update(cc, args):
    """Update a region that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in regions.REGION_FIELDS and not (v is None)}
    item_id = fields.pop('id')
    if not fields:
        raise exc.CommandError(
            'Nothing to update... Please specify one or more of --name, or '
            '--note'
        )
    region = cc.regions.update(item_id, **fields)
    data = {f: getattr(region, f, '') for f in regions.REGION_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region.')
def do_region_delete(cc, args):
    """Delete a region that is registered with the Craton service."""
    try:
        response = cc.regions.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete region {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Region {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID or name of the region.')
@cliutils.arg('--format',
              metavar='<format>',
              help='Output format of variables.')
@cliutils.error('getting variables')
def do_region_vars_get(cc, args):
    """Get variables for a region."""
    region = cc.regions.get(item_id=args.id)
    cliutils.get_and_print_variables(region, args)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region.')
@cliutils.arg('variables', nargs=argparse.REMAINDER)
@cliutils.error('setting variables')
def do_region_vars_set(cc, args):
    """Set variables for a region."""
    region = cc.regions.get(item_id=args.id)
    cliutils.set_variables(region, args)
