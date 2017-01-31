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
"""Network Devices resource and resource shell wrapper."""
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import network_devices


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
              required=True,
              help='Region of the network device.')
@cliutils.arg('-d', '--device-type',
              metavar='<devicetype>',
              required=True,
              help='Device Type of the network device.')
@cliutils.arg('--ip-address',
              metavar='<ip>',
              required=True,
              help='IP address for the network device.')
@cliutils.arg('--active',
              metavar='<active>',
              required=False,
              help='Netmaks of the network.')
def do_network_device_create(cc, args):
    """Register a new network device with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in network_devices.NETWORK_DEVICE_FIELDS
              and not (v is None)}

    nd = cc.network_devices.create(**fields)
    data = {f: getattr(nd, f, '')
            for f in network_devices.NETWORK_DEVICE_FIELDS}
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
def do_network_device_list(cc, args):
    """List all network devices."""
    params = {}
    default_fields = ['id', 'name', 'device_type', 'active',
                      'region_id', 'cell_id']
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
        fields = network_devices.NETWORK_DEVICE_FIELDS
        params['detail'] = args.detail
    elif args.fields:
        try:
            fields = {x: network_devices.NETWORK_DEVICE_FIELDS[x]
                      for x in args.fields}
        except KeyError as keyerr:
            raise exc.CommandError('Invalid field "{}"'.format(keyerr.args[0]))
    else:
        fields = {x: network_devices.NETWORK_DEVICE_FIELDS[x]
                  for x in default_fields}
    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in network_devices.NETWORK_DEVICE_FIELDS:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(
                    args.sort_key, network_devices.NETWORK_DEVICE_FIELDS()
                )
            )
        params['sort_key'] = sort_key
    params['sort_dir'] = args.sort_dir

    nds = cc.network_devices.list(**params)
    cliutils.print_list(nds, list(fields))


@cliutils.arg('id',
              metavar='<networkdevices>',
              type=int,
              help='ID of the network device.')
def do_network_device_show(cc, args):
    """Show detailed information about a network device."""
    nd = cc.network_devices.get(args.id)
    data = {f: getattr(nd, f, '')
            for f in network_devices.NETWORK_DEVICE_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<device>',
              type=int,
              help='ID of the device.')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the host.')
@cliutils.arg('-i', '--ip_address',
              metavar='<ipaddress>',
              help='IP Address of the host.')
@cliutils.arg('--device-type',
              dest='device_type',
              metavar='<device_type>',
              help='Type of device.')
@cliutils.arg('--model',
              dest='model_name',
              metavar='<model_name>',
              help='Model name of the device.')
@cliutils.arg('--os-version',
              dest='os_version',
              metavar='<os_version>',
              help='OS version of the device.')
@cliutils.arg('-a', '--active',
              default=True,
              help='Status of the host.  Active or inactive.')
def do_network_device_update(cc, args):
    """Update a network device that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in network_devices.NETWORK_DEVICE_FIELDS
              and (v or v is False)}
    item_id = fields.pop('id')
    host = cc.network_devices.update(item_id, **fields)
    print("Device {0} has been successfully updated.".format(host.id))
    data = {f: getattr(host, f, '')
            for f in network_devices.NETWORK_DEVICE_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<device>',
              type=int,
              help='ID of the network device.')
def do_network_device_delete(cc, args):
    """Delete a network device that is registered with the Craton service."""
    try:
        response = cc.network_devices.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete network device {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Device {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
