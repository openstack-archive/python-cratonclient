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
from cratonclient.common import cliutils

HOST_FIELDS = ['id', 'name', 'type', 'active', 'project_id', 'region_id',
               'cell_id', 'note', 'access_secret_id', 'ip_address']


@cliutils.arg('host',
              metavar='<host>',
              type=int,
              help='Name or ID of the host.')
def do_host_show(cc, args):
    """Show detailed information about a host."""
    host = cc.hosts.get(args.host)
    data = dict([(f, getattr(host, f, '')) for f in HOST_FIELDS])
    cliutils.print_dict(data, wrap=72)


def do_host_list(cc, args):
    """Print list of hosts which are registered with the Craton service."""
    params = {}
    columns = ['id', 'name']
    hosts = cc.hosts.list(args.craton_project_id, **params)
    cliutils.print_list(hosts, columns)


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the host.')
@cliutils.arg('-i', '--ip_address',
              metavar='<ipaddress>',
              required=True,
              help='IP Address of the host.')
@cliutils.arg('-p', '--project',
              dest='project_id',
              metavar='<project>',
              type=int,
              required=True,
              help='ID of the project that the host belongs to.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              required=True,
              help='ID of the region that the host belongs to.')
@cliutils.arg('-c', '--cell',
              dest='cell_id',
              metavar='<cell>',
              type=int,
              help='ID of the cell that the host belongs to.')
@cliutils.arg('-a', '--active',
              default=True,
              help='Status of the host.  Active or inactive.')
@cliutils.arg('-t', '--type',
              help='Type of the host.')
@cliutils.arg('--note',
              help='Note about the host.')
@cliutils.arg('--access_secret',
              type=int,
              dest='access_secret_id',
              metavar='<access_secret>',
              help='ID of the access secret of the host.')
@cliutils.arg('-l', '--labels',
              default=[],
              help='List of labels for the host.')
def do_host_create(cc, args):
    """Register a new host with the Craton service."""
    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in HOST_FIELDS and not (v is None))

    host = cc.hosts.create(**fields)
    data = dict([(f, getattr(host, f, '')) for f in HOST_FIELDS])
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('host',
              metavar='<host>',
              type=int,
              help='ID of the host.')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the host.')
@cliutils.arg('-i', '--ip_address',
              metavar='<ipaddress>',
              help='IP Address of the host.')
@cliutils.arg('-p', '--project',
              dest='project_id',
              metavar='<project>',
              type=int,
              help='ID of the project that the host belongs to.')
@cliutils.arg('-r', '--region',
              dest='region_id',
              metavar='<region>',
              type=int,
              help='ID of the region that the host belongs to.')
@cliutils.arg('-c', '--cell',
              dest='cell_id',
              metavar='<cell>',
              type=int,
              help='ID of the cell that the host belongs to.')
@cliutils.arg('-a', '--active',
              default=True,
              help='Status of the host.  Active or inactive.')
@cliutils.arg('-t', '--type',
              help='Type of the host.')
@cliutils.arg('--note',
              help='Note about the host.')
@cliutils.arg('--access_secret',
              dest='access_secret_id',
              metavar='<access_secret>',
              type=int,
              help='ID of the access secret of the host.')
@cliutils.arg('-l', '--labels',
              default=[],
              help='List of labels for the host.')
def do_host_update(cc, args):
    """Update a host that is registered with the Craton service."""
    host = cc.hosts.update(args)
    print("Host {0} has been successfully update.".format(host.id))
