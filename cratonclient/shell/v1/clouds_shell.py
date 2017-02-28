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
from cratonclient.v1 import clouds


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the host.')
@cliutils.arg('--note',
              help='Note about the host.')
def do_cloud_create(cc, args):
    """Register a new cloud with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in clouds.CLOUD_FIELDS and not (v is None)}

    cloud = cc.clouds.create(**fields)
    args.formatter.configure(wrap=72).handle(cloud)


@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=[],
              help='Comma-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'Can not be used when "--detail" is specified')
@cliutils.arg('--all',
              action='store_true',
              default=False,
              help='Retrieve and show all clouds. This will override '
                   'the provided value for --limit and automatically '
                   'retrieve each page of results.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of clouds to return.')
@cliutils.arg('--marker',
              metavar='<marker>',
              default=None,
              help='ID of the cell to use to resume listing clouds.')
def do_cloud_list(cc, args):
    """List all clouds."""
    params = {}
    default_fields = ['id', 'name']
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit
    if args.all is True:
        params['limit'] = 100

    if args.fields:
        try:
            fields = {x: clouds.CLOUD_FIELDS[x] for x in args.fields}
        except KeyError as err:
            raise exc.CommandError('Invalid field "{}"'.format(err.args[0]))
    else:
        fields = default_fields
    params['marker'] = args.marker
    params['autopaginate'] = args.all

    clouds_list = cc.clouds.list(**params)
    args.formatter.configure(fields=list(fields)).handle(clouds_list)


@cliutils.arg('id',
              metavar='<cloud>',
              type=int,
              help='ID of the cloud.')
def do_cloud_show(cc, args):
    """Show detailed information about a cloud."""
    cloud = cc.clouds.get(args.id)
    args.formatter.configure(wrap=72).handle(cloud)


@cliutils.arg('id',
              metavar='<cloud>',
              type=int,
              help='ID of the cloud')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the cloud.')
@cliutils.arg('--note',
              help='Note about the cloud.')
def do_cloud_update(cc, args):
    """Update a cloud that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in clouds.CLOUD_FIELDS and not (v is None)}
    item_id = fields.pop('id')
    if not fields:
        raise exc.CommandError(
            'Nothing to update... Please specify one or more of --name, or '
            '--note'
        )
    cloud = cc.clouds.update(item_id, **fields)
    args.formatter.configure(wrap=72).handle(cloud)


@cliutils.arg('id',
              metavar='<cloud>',
              type=int,
              help='ID of the cloud.')
def do_cloud_delete(cc, args):
    """Delete a cloud that is registered with the Craton service."""
    try:
        response = cc.clouds.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete cloud {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Cloud {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
