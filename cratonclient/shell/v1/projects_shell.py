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
"""Projects resource and resource shell wrapper."""
from __future__ import print_function

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import projects


@cliutils.arg('id',
              metavar='<project>',
              help='ID of the project.')
def do_project_show(cc, args):
    """Show detailed information about a project."""
    project = cc.projects.get(args.id)
    data = {f: getattr(project, f, '') for f in projects.PROJECT_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('-n', '--name',
              metavar='<name>',
              help='Name of the project.')
@cliutils.arg('--detail',
              action='store_true',
              default=False,
              help='Show detailed information about the projects.')
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
              help='Retrieve and show all projects. This will override '
                   'the provided value for --limit and automatically '
                   'retrieve each page of results.')
@cliutils.arg('--limit',
              metavar='<limit>',
              type=int,
              help='Maximum number of projects to return.')
@cliutils.arg('--marker',
              metavar='<marker>',
              default=None,
              help='ID of the cell to use to resume listing projects.')
def do_project_list(cc, args):
    """Print list of projects which are registered with the Craton service."""
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

    if args.fields and args.detail:
        raise exc.CommandError('Cannot specify both --fields and --detail.')

    if args.name:
        params['name'] = args.name
    if args.detail:
        fields = projects.PROJECT_FIELDS
    elif args.fields:
        try:
            fields = {x: projects.PROJECT_FIELDS[x] for x in args.fields}
        except KeyError as keyerr:
            raise exc.CommandError('Invalid field "{}"'.format(keyerr.args[0]))
    else:
        fields = {x: projects.PROJECT_FIELDS[x] for x in default_fields}
    params['marker'] = args.marker
    params['autopaginate'] = args.all

    listed_projects = cc.projects.list(**params)
    cliutils.print_list(listed_projects, list(fields))


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the project.')
def do_project_create(cc, args):
    """Register a new project with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in projects.PROJECT_FIELDS and not (v is None)}
    project = cc.projects.create(**fields)
    data = {f: getattr(project, f, '') for f in projects.PROJECT_FIELDS}
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('id',
              metavar='<project>',
              help='ID of the project.')
def do_project_delete(cc, args):
    """Delete a project that is registered with the Craton service."""
    try:
        response = cc.projects.delete(args.id)
    except exc.ClientException as client_exc:
        raise exc.CommandError(
            'Failed to delete project {} due to "{}:{}"'.format(
                args.id, client_exc.__class__, str(client_exc)
            )
        )
    else:
        print("Project {0} was {1} deleted.".
              format(args.id, 'successfully' if response else 'not'))
