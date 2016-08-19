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

from cratonclient.common import cliutils
from cratonclient.v1.regions import REGION_FIELDS as r_fields


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the host.')
@cliutils.arg('--note',
              help='Note about the host.')
def do_region_create(cc, args):
    """Register a new region with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in r_fields and not (v is None)}

    region = cc.regions.create(**fields)
    data = {f: getattr(region, f, '') for f in r_fields}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region.')
def do_region_show(cc, args):
    """Show detailed information about a region."""
    region = cc.regions.get(args.id)
    data = {f: getattr(region, f, '') for f in r_fields}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region')
@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the region.')
@cliutils.arg('-p', '--project',
              dest='project_id',
              metavar='<project_id>',
              type=int,
              help='ID of the project that the region belongs to.')
@cliutils.arg('--note',
              help='Note about the region.')
def do_region_update(cc, args):
    """Update a region that is registered with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in r_fields and not (v is None)}
    region = cc.regions.update(**fields)
    data = {f: getattr(region, f, '') for f in r_fields}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<region>',
              type=int,
              help='ID of the region.')
def do_region_delete(cc, args):
    """Delete a region that is registered with the Craton service."""
    response = cc.regions.delete(args.id)
    print("Region {0} was {1}successfully deleted.".
          format(args.id, '' if response else 'un'))
