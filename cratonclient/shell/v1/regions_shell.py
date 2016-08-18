"""Hosts resource and resource shell wrapper."""

from cratonclient.common import cliutils
from cratonclient.v1.regions import REGION_FIELDS as r_fields


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the host.')
@cliutils.arg('-p', '--project',
              dest='project_id',
              metavar='<project>',
              type=int,
              help='ID of the project that the host belongs to.')
@cliutils.arg('--note',
              help='Note about the host.')
def do_region_create(cc, args):
    """Register a new region with the Craton service."""
    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in r_fields and not (v is None))

    region = cc.regions.create(**fields)
    data = dict([(f, getattr(region, f, '')) for f in r_fields])
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('region_id',
              metavar='<region_id>',
              type=int,
              help='ID of the region.')
def do_region_show(cc, args):
    """Show detailed information about a region."""
    region = cc.regions.get(args.region_id)
    data = dict([(f, getattr(region, f, '')) for f in r_fields])
    cliutils.print_dict(data, wrap=72)