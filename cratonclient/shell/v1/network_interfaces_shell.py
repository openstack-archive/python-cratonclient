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
"""Network Interface resource and resource shell wrapper."""
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import network_interfaces


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the network device.')
@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              required=False,
              help='Cell of the network device.')
@cliutils.arg('-r', '--region',
              metavar='<region>',
              required=False,
              help='Region of the network device.')
@cliutils.arg('-d', '--device-id',
              metavar='<device_id>',
              type=int,
              required=True,
              help='Device Id of the device for the interface.')
@cliutils.arg('--network-id',
              metavar='<network_id>',
              type=int,
              required=False,
              help='Netowrk Id of the device for the interface.')
@cliutils.arg('--vlan-id',
              metavar='<vlan_id>',
              type=int,
              required=False,
              help='Vlan Id of the device for the interface.')
@cliutils.arg('--vlan',
              metavar='<vlan>',
              required=False,
              help='Vlan of the device for the interface.')
@cliutils.arg('-i', '--ip-address',
              metavar='<ip>',
              required=True,
              help='IP address for the network device.')
@cliutils.arg('--interface-type',
              metavar='<interface_type>',
              required=False,
              help='Type of interface.')
@cliutils.arg('--link',
              metavar='<link>',
              required=False,
              help='Link status of the interfae.')
@cliutils.arg('--duplex',
              metavar='<duplex>',
              required=False,
              help='Duplex value of the interface.')
@cliutils.arg('--port',
              metavar='<port>',
              required=False,
              help='Port value of the interface.')
def do_network_interface_create(cc, args):
    """Register a new network interface with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in network_interfaces.NETWORK_INTERFACE_FIELDS
              and not (v is None)}

    nd = cc.network_interfaces.create(**fields)
    data = {f: getattr(nd, f, '')
            for f in network_interfaces.NETWORK_INTERFACE_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              required=False,
              help='Cell of the network device.')
@cliutils.arg('-r', '--region',
              metavar='<region>',
              required=False,
              help='Region of the network device.')
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
              choices=('asc', 'desc'),
              help='Sort direction: "asc" (default) or "desc".')
@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=[],
              help='Comma-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'Can not be used when "--detail" is specified')
def do_network_interface_list(cc, args):
    """List all network interfaces."""
    params = {}
    default_fields = ['id', 'name', 'device_id', 'network_id',
                      'ip_address', 'vlan']
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
        fields = network_interfaces.NETWORK_INTERFACE_FIELDS
        params['detail'] = args.detail
    elif args.fields:
        try:
            fields = {x: network_interfaces.NETWORK_INTERFACE_FIELDS[x]
                      for x in args.fields}
        except KeyError as keyerr:
            raise exc.CommandError('Invalid field "{}"'.format(keyerr.args[0]))
    else:
        fields = {x: network_interfaces.NETWORK_INTERFACE_FIELDS[x]
                  for x in default_fields}
    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in network_interfaces.NETWORK_INTERFACE_FIELDS:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(
                    args.sort_key,
                    network_interfaces.NETWORK_INTERFACE_FIELDS()
                )
            )
        params['sort_key'] = sort_key
    params['sort_dir'] = args.sort_dir

    nds = cc.network_interfaces.list(**params)
    cliutils.print_list(nds, list(fields))


@cliutils.arg('id',
              metavar='<network_interface>',
              type=int,
              help='ID of the network device.')
def do_network_interface_show(cc, args):
    """Show detailed information about a network device."""
    nd = cc.network_interfaces.get(args.id)
    data = {f: getattr(nd, f, '')
            for f in network_interfaces.NETWORK_INTERFACE_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<network_interface>',
              type=int,
              help='ID of the device.')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the host.')
@cliutils.arg('-d', '--device-id',
              metavar='<device_id>',
              type=int,
              required=False,
              help='Device Id of the device for the interface.')
@cliutils.arg('--network-id',
              metavar='<network_id>',
              type=int,
              required=False,
              help='Netowrk Id of the device for the interface.')
@cliutils.arg('--vlan-id',
              metavar='<vlan_id>',
              type=int,
              required=False,
              help='Vlan Id of the device for the interface.')
@cliutils.arg('--vlan',
              metavar='<vlan>',
              required=False,
              help='Vlan of the device for the interface.')
@cliutils.arg('-i', '--ip-address',
              metavar='<ip>',
              required=False,
              help='IP address for the network device.')
@cliutils.arg('--interface-type',
              metavar='<interface_type>',
              required=False,
              help='Type of interface.')
@cliutils.arg('--link',
              metavar='<link>',
              required=False,
              help='Link status of the interfae.')
@cliutils.arg('--duplex',
              metavar='<duplex>',
              required=False,
              help='Duplex value of the interface.')
@cliutils.arg('--port',
              metavar='<port>',
              required=False,
              help='Port value of the interface.')
def do_network_interface_update(cc, args):
    """Update a network interface that is registered with Craton."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in network_interfaces.NETWORK_INTERFACE_FIELDS
              and (v or v is False)}
    item_id = fields.pop('id')
    host = cc.network_interfaces.update(item_id, **fields)
    print("Device {0} has been successfully updated.".format(host.id))
    data = {f: getattr(host, f, '')
            for f in network_interfaces.NETWORK_INTERFACE_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<network_interface>',
              type=int,
              help='ID of the network interface.')
def do_network_interface_delete(cc, args):
    """Delete a network interface that is registered with Craton."""
    try:
        response = cc.network_interfaces.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete network device {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Device {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
