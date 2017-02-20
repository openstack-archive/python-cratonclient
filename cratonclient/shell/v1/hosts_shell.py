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
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import hosts


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID of the host.')
def do_host_show(cc, args):
    """Show detailed information about a host."""
    host = cc.hosts.get(args.id)
    args.formatter.configure(wrap=72).handle(host)


@cliutils.arg('-r', '--region',
              metavar='<region>',
              type=int,
              required=True,
              help='ID of the region that the host belongs to.')
@cliutils.arg('--cloud',
              metavar='<cloud>',
              type=int,
              help='ID of the cloud that the host belongs to.')
@cliutils.arg('-c', '--cell',
              metavar='<cell>',
              type=int,
              help='Integer ID of the cell that contains '
                   'the desired list of hosts.')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Show detailed information about the hosts.')
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
@cliutils.arg('--all',
              action='store_true',
              default=False,
              help='Retrieve and show all hosts. This will override '
                   'the provided value for --limit and automatically '
                   'retrieve each page of results.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of hosts to return.')
@cliutils.arg('--marker',
              metavar='<marker>',
              default=None,
              help='ID of the cell to use to resume listing hosts.')
def do_host_list(cc, args):
    """Print list of hosts which are registered with the Craton service."""
    params = {}
    default_fields = [
        'id', 'name', 'device_type', 'active', 'region_id', 'cell_id']
    if args.cell is not None:
        params['cell_id'] = args.cell
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

    if args.fields and args.detail:
        raise exc.CommandError('Cannot specify both --fields and --detail.')

    if args.detail:
        fields = hosts.HOST_FIELDS
        params['detail'] = args.detail
    elif args.fields:
        try:
            fields = {x: hosts.HOST_FIELDS[x] for x in args.fields}
        except KeyError as keyerr:
            raise exc.CommandError('Invalid field "{}"'.format(keyerr.args[0]))
    else:
        fields = {x: hosts.HOST_FIELDS[x] for x in default_fields}
    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in hosts.HOST_FIELDS:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(
                    args.sort_key, hosts.HOST_FIELDS.keys()
                )
            )
        params['sort_key'] = sort_key
    params['sort_dir'] = args.sort_dir
    params['region_id'] = args.region
    params['marker'] = args.marker
    params['autopaginate'] = args.all

    host_list = cc.hosts.list(**params)
    args.formatter.configure(fields=list(fields)).handle(host_list)


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the host.')
@cliutils.arg('-i', '--ip_address',
              metavar='<ipaddress>',
              required=True,
              help='IP Address of the host.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              required=True,
              help='ID of the region that the host belongs to.')
@cliutils.arg('--cloud',
              dest='cloud_id',
              metavar='<cloud>',
              type=int,
              required=True,
              help='ID of the cloud that the host belongs to.')
@cliutils.arg('-c', '--cell',
              dest='cell_id',
              metavar='<cell>',
              type=int,
              help='ID of the cell that the host belongs to.')
@cliutils.arg('-t', '--type',
              dest='device_type',
              metavar='<type>',
              required=True,
              help='Type of the host.')
@cliutils.arg('-a', '--active',
              default=True,
              help='Status of the host.  Active or inactive.')
@cliutils.arg('--note',
              help='Note about the host.')
@cliutils.arg('-l', '--labels',
              default=[],
              help='List of labels for the host.')
def do_host_create(cc, args):
    """Register a new host with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in hosts.HOST_FIELDS and (v or v is False)}
    host = cc.hosts.create(**fields)
    args.formatter.configure(wrap=72).handle(host)


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID of the host.')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the host.')
@cliutils.arg('-i', '--ip_address',
              metavar='<ipaddress>',
              help='IP Address of the host.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              help='Desired ID of the region that the host should change to.')
@cliutils.arg('--cloud',
              dest='cloud_id',
              metavar='<cloud>',
              type=int,
              help='Desired ID of the cloud that the host should change to.')
@cliutils.arg('-c', '--cell',
              dest='cell_id',
              metavar='<cell>',
              type=int,
              help='ID of the cell that the host belongs to.')
@cliutils.arg('-a', '--active',
              default=True,
              help='Status of the host.  Active or inactive.')
@cliutils.arg('--note',
              help='Note about the host.')
@cliutils.arg('-l', '--labels',
              default=[],
              help='List of labels for the host.')
def do_host_update(cc, args):
    """Update a host that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in hosts.HOST_FIELDS and (v or v is False)}
    item_id = fields.pop('id')
    host = cc.hosts.update(item_id, **fields)
    print("Host {0} has been successfully updated.".format(host.id))
    args.formatter.configure(wrap=72).handle(host)


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID of the host.')
def do_host_delete(cc, args):
    """Delete a host that is registered with the Craton service."""
    try:
        response = cc.hosts.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete host {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Host {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
