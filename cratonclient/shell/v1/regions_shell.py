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

from cratonclient.common import cliutils
from cratonclient import exceptions as exc

DEFAULT_REGION_FIELDS = [
    'id',
    'name',
    'cloud_id',
]

REGION_FIELDS = DEFAULT_REGION_FIELDS + [
    'project_id',
    'note',
    'created_at',
    'updated_at',
]


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the host.')
@cliutils.arg('--cloud',
              dest='cloud_id',
              metavar='<cloud>',
              type=int,
              required=True,
              help='ID of the cloud that the region belongs to.')
@cliutils.arg('--note',
              help='Note about the host.')
def do_region_create(cc, args):
    """Register a new region with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in REGION_FIELDS and not (v is None)}

    region = cc.regions.create(**fields)
    args.formatter.configure(wrap=72).handle(region)


@cliutils.arg('--cloud',
              metavar='<cloud>',
              type=int,
              help='ID of the cloud that the region belongs to.')
@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=DEFAULT_REGION_FIELDS,
              help='Space-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'Can not be used when "--detail" is specified')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Show detailed information about the regions.')
@cliutils.arg('--all',
              action='store_true',
              default=False,
              help='Retrieve and show all regions. This will override '
                   'the provided value for --limit and automatically '
                   'retrieve each page of results.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of regions to return.')
@cliutils.arg('--marker',
              metavar='<marker>',
              default=None,
              help='ID of the region to use to resume listing regions.')
@cliutils.arg('--vars',
              metavar='<vars>',
              nargs='+',
              action='append',
              default=[],
              help='Variables to use as filter in the form of '
                   '--vars="key:value" --vars="key2:value2"')
def do_region_list(cc, args):
    """List all regions."""
    params = {}
    if args.vars:
        query_vars = ",".join([i[0] for i in args.vars])
        params['vars'] = query_vars
    if args.cloud is not None:
        params['cloud_id'] = args.cloud
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit
    if args.all is True:
        params['limit'] = 100

    if args.detail:
        if args.fields and args.fields == DEFAULT_REGION_FIELDS:
            args.fields = REGION_FIELDS
        else:
            raise exc.CommandError(
                'Cannot specify both --fields and --detail.'
            )
        params['detail'] = args.detail

    fields = args.fields
    for field in args.fields:
        if field not in REGION_FIELDS:
            raise exc.CommandError(
                'Invalid field "{}"'.format(field)
            )

    params['marker'] = args.marker
    params['autopaginate'] = args.all

    regions_list = cc.regions.list(**params)
    args.formatter.configure(fields=list(fields)).handle(regions_list)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region.')
def do_region_show(cc, args):
    """Show detailed information about a region."""
    region = cc.regions.get(args.id)
    args.formatter.configure(wrap=72).handle(region)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the region.')
@cliutils.arg('--cloud',
              dest='cloud_id',
              metavar='<cloud>',
              type=int,
              help='Desired ID of the cloud that the region should change to.')
@cliutils.arg('--note',
              help='Note about the region.')
def do_region_update(cc, args):
    """Update a region that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in REGION_FIELDS and not (v is None)}
    item_id = fields.pop('id')
    if not fields:
        raise exc.CommandError(
            'Nothing to update... Please specify one or more of --name, '
            '--cloud, or --note'
        )
    region = cc.regions.update(item_id, **fields)
    args.formatter.configure(wrap=72).handle(region)


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
