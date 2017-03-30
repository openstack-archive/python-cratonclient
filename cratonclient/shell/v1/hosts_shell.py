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

import argparse
import sys

from cratonclient.common import cliutils
from cratonclient import exceptions as exc


DEFAULT_HOST_FIELDS = [
    'id',
    'name',
    'active',
    'device_type',
    'ip_address',
    'cloud_id',
    'region_id',
    'cell_id',
    'created_at',
]

HOST_FIELDS = DEFAULT_HOST_FIELDS + [
    'updated_at',
    'note',
    'variables',
    'labels',
    'parent_id',
    'project_id',
]


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID of the host.')
@cliutils.arg('--fields',
              metavar='<fields>',
              action='append',
              help='Comma-separated list of fields to display. '
                   'Only these fields will be fetched from the server. '
                   'Can not be used when "--detail" is specified')
def do_host_show(cc, args):
    """Show detailed information about a host."""
    host = cc.hosts.get(args.id)
    if not args.fields:
        fields = None
    else:
        fields = cliutils.comma_arg_flattener(args.fields)
        for field in fields:
            if field not in HOST_FIELDS:
                raise exc.CommandError(
                    'Invalid field "{}"'.format(field)
                    )
    args.formatter.configure(wrap=72, fields=fields).handle(host)


@cliutils.arg('-r', '--region',
              metavar='<region>',
              type=int,
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
              metavar='<fields>',
              action='append',
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
@cliutils.arg('--device-type',
              metavar='<device_type>',
              default=None,
              help='Device type to use as filter.')
@cliutils.arg('--vars',
              metavar='<vars>',
              default=None,
              help='Variables to use as filter in the form of key:value.')
@cliutils.arg('--label',
              metavar='<label>',
              default=None,
              help='Label to use as filter.')
@cliutils.arg('--ip',
              metavar='<ip_address>',
              default=None,
              help='IP address to use as filter.')
def do_host_list(cc, args):
    """Print list of hosts which are registered with the Craton service."""
    params = {}
    if args.cell is not None:
        params['cell_id'] = args.cell
    if args.cloud is not None:
        params['cloud_id'] = args.cloud
    if args.device_type is not None:
        params['device_type'] = args.device_type
    if args.vars is not None:
        params['vars'] = args.vars
    if args.label is not None:
        params['label'] = args.label
    if args.ip is not None:
        params['ip_address'] = args.ip
    if args.limit is not None:
        if args.limit < 0:
            raise exc.CommandError('Invalid limit specified. Expected '
                                   'non-negative limit, got {0}'
                                   .format(args.limit))
        params['limit'] = args.limit
    if args.all is True:
        params['limit'] = 100

    if args.detail and args.fields is not None:
        raise exc.CommandError('Cannot specify both --fields and --detail.')
    elif args.detail:
        fields = HOST_FIELDS
        params['details'] = args.detail
    elif args.fields is not None:
        fields = cliutils.comma_arg_flattener(args.fields)
        # NOTE(anonymike): In order to get all variables a details call must
        # be made to the api.
        params['details'] = True
        for field in fields:
            if field not in HOST_FIELDS:
                raise exc.CommandError(
                    'Invalid field "{}"'.format(field)
                )
    else:
        fields = DEFAULT_HOST_FIELDS

    sort_key = args.sort_key and args.sort_key.lower()
    if sort_key is not None:
        if sort_key not in HOST_FIELDS:
            raise exc.CommandError(
                '{0} is an invalid key for sorting,  valid values for '
                '--sort-key are: {1}'.format(
                    args.sort_key, HOST_FIELDS
                )
            )
        params['sort_key'] = sort_key
    if args.region is not None:
        params['region_id'] = args.region

    params['sort_dir'] = args.sort_dir
    params['marker'] = args.marker
    params['autopaginate'] = args.all

    host_list = cc.hosts.list(**params)
    args.formatter.configure(fields=fields).handle(host_list)


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
              if k in HOST_FIELDS and (v or v is False)}
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
              if k in HOST_FIELDS and (v or v is False)}
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
            'Failed to delete cell {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc),
            )
        )
    else:
        print("Host {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID or name of the host.')
@cliutils.handle_shell_exception
def do_host_vars_get(cc, args):
    """Get variables for a host."""
    variables = cc.hosts.get(args.id).variables.get()
    formatter = args.formatter.configure(dict_property="Variable", wrap=72)
    formatter.handle(variables)


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID of the host.')
@cliutils.arg('variables', nargs=argparse.REMAINDER)
@cliutils.handle_shell_exception
def do_host_vars_set(cc, args):
    """Set variables for a host."""
    host_id = args.id
    if not args.variables and sys.stdin.isatty():
        raise exc.CommandError(
            'Nothing to update... Please specify variables to set in the '
            'following format: "key=value". You may also specify variables to '
            'delete by key using the format: "key="'
        )
    adds, deletes = cliutils.variable_updates(args.variables)
    variables = cc.hosts.get(host_id).variables
    if deletes:
        variables.delete(*deletes)
    variables.update(**adds)
    formatter = args.formatter.configure(wrap=72, dict_property="Variable")
    formatter.handle(variables.get())


@cliutils.arg('id',
              metavar='<host>',
              type=int,
              help='ID of the host.')
@cliutils.arg('variables', nargs=argparse.REMAINDER)
@cliutils.handle_shell_exception
def do_host_vars_delete(cc, args):
    """Delete variables for a host by key."""
    host_id = args.id
    if not args.variables and sys.stdin.isatty():
        raise exc.CommandError(
            'Nothing to delete... Please specify variables to delete by '
            'listing the keys you wish to delete separated by spaces.'
        )
    deletes = cliutils.variable_deletes(args.variables)
    variables = cc.hosts.get(host_id).variables
    response = variables.delete(*deletes)
    print("Variables {0} deleted.".
          format('successfully' if response else 'not'))
