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
"""Networks resource and resource shell wrapper."""
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import networks


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the network.')
@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              required=False,
              help='Cell of the network.')
@cliutils.arg('-r', '--region',
              metavar='<region>',
              required=True,
              help='Region of the network.')
@cliutils.arg('--cidr',
              metavar='<cidr>',
              required=True,
              help='cidr of the network.')
@cliutils.arg('--gateway',
              metavar='<gateway>',
              required=True,
              help='Gateway for the network.')
@cliutils.arg('--netmask',
              metavar='<netmask>',
              required=True,
              help='Netmaks of the network.')
@cliutils.arg('--ip-block-type',
              metavar='<blocktype>',
              required=True,
              help='IP block type of the network.')
def do_network_create(cc, args):
    """Register a new network with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in networks.NETWORKS_FIELDS and not (v is None)}

    network = cc.networks.create(**fields)
    data = {f: getattr(network, f, '') for f in network.NETWORKS_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of networks to return.')
@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              required=False,
              help='Cell of the network.')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Show detailed information about the hosts.')
@cliutils.arg('-r', '--region',
              metavar='<region>',
              required=False,
              help='Region of the network.')
@cliutils.arg('--sort-key',
              metavar='<field>',
              help='Host field that will be used for sorting.')
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
def do_network_list(cc, args):
    """List all networks."""
    params = {}
    default_fields = ['id', 'name', 'region_id', 'cidr']
    if args.region is not None:
        params['region_id'] = args.region
    if args.cell is not None:
        params['cell_id'] = args.cell
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit

    if args.fields and args.detail:
        raise exc.CommandError('Cannot specify both --fields and --detail.')

    if args.detail:
        fields = networks.NETWORKS_FIELDS
        params['detail'] = args.detail
    elif args.fields:
        try:
            fields = {x: networks.NETWORKS_FIELDS[x] for x in args.fields}
        except KeyError as keyerr:
            raise exc.CommandError('Invalid field "{}"'.format(keyerr.args[0]))
    else:
        fields = {x: networks.NETWORKS_FIELDS[x] for x in default_fields}
    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in networks.NETWORKS_FIELDS:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(
                    args.sort_key, networks.NETWORKS_FIELDS.keys()
                )
            )
        params['sort_key'] = sort_key
    params['sort_dir'] = args.sort_dir

    networks_list = cc.networks.list(**params)
    cliutils.print_list(networks_list, list(fields))


@cliutils.arg('id',
              metavar='<network>',
              type=int,
              help='ID of the network.')
def do_network_show(cc, args):
    """Show detailed information about a network."""
    network = cc.networks.get(args.id)
    data = {f: getattr(network, f, '') for f in networks.NETWORKS_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<network>',
              type=int,
              help='ID of the network')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the network.')
@cliutils.arg('--ip-block-type',
              metavar='<ipblocktype>',
              help='IP block of the network.')
def do_network_update(cc, args):
    """Update a network that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in networks.NETWORKS_FIELDS and not (v is None)}
    item_id = fields.pop('id')
    if not fields:
        raise exc.CommandError(
            'Nothing to update... Please specify one or more of --name, or '
            '--ip-block-type'
        )
    network = cc.networks.update(item_id, **fields)
    data = {f: getattr(network, f, '') for f in networks.NETWORKS_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<network>',
              type=int,
              help='ID of the network.')
def do_network_delete(cc, args):
    """Delete a network  that is registered with the Craton service."""
    try:
        response = cc.netowks.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete network {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Network {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
