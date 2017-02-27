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
from cratonclient.v1 import devices


@cliutils.arg('--fields',
              nargs='+',
              metavar='<fields>',
              default=[],
              help='Space-separated list of fields to display. '
                   'Only these fields will be fetched from the server.')
@cliutils.arg('--all',
              action='store_true',
              default=False,
              help='Retrieve and show all devices. This will override '
                   'the provided value for --limit and automatically '
                   'retrieve each page of results.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of devices to return.')
@cliutils.arg('--marker',
              metavar='<marker>',
              default=None,
              help='ID of the device to use to resume listing devices.')
@cliutils.arg('--parent-id',
              metavar='<parentid>',
              default=None,
              help='Parent ID of required devices.')
@cliutils.arg('--descendants',
              default=False,
              action='store_true',
              help='When parent_id is also specified, include all descendants.'
              )
def do_device_list(cc, args):
    """List all devices."""
    params = {}
    default_fields = ['id', 'name', 'device_type', 'parent_id']
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
            fields = {x: devices.DEVICE_FIELDS[x] for x in args.fields}
        except KeyError as err:
            raise exc.CommandError('Invalid field "{}"'.format(err.args[0]))
    else:
        fields = default_fields
    params['marker'] = args.marker
    params['autopaginate'] = args.all
    if args.parent_id:
        params['parent_id'] = args.parent_id
    if args.descendants:
        params['descendants'] = args.descendants

    devices_list = cc.devices.list(**params)
    cliutils.print_list(devices_list, list(fields))
