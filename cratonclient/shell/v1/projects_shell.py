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

import argparse

from cratonclient.common import cliutils
from cratonclient import exceptions as exc
from cratonclient.v1 import projects


@cliutils.arg('id',
              metavar='<project>',
              help='ID of the project.')
def do_project_show(cc, args):
    """Show detailed information about a project."""
    project = cc.projects.get(args.id)
    args.formatter.configure(wrap=72).handle(project)


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
              help='Space-separated list of fields to display. '
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
    args.formatter.configure(fields=list(fields)).handle(listed_projects)


@cliutils.arg('-n', '--name',
              metavar='<name>',
              required=True,
              help='Name of the project.')
def do_project_create(cc, args):
    """Register a new project with the Craton service."""
    fields = {k: v for (k, v) in vars(args).items()
              if k in projects.PROJECT_FIELDS and not (v is None)}
    project = cc.projects.create(**fields)
    args.formatter.configure(wrap=72).handle(project)


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


@cliutils.arg('id',
              metavar='<project>',
              help='ID or name of the project.')
@cliutils.handle_shell_exception
def do_project_vars_get(cc, args):
    """Get variables for a project."""
    args.formatter.configure(dict_property="Variable", wrap=72) \
        .handle(cc.projects.get(args.id).variables.get())


@cliutils.arg('id',
              metavar='<project>',
              help='ID of the project.')
@cliutils.arg('variables', nargs=argparse.REMAINDER)
@cliutils.handle_shell_exception
def do_project_vars_set(cc, args):
    """Set variables for a project."""
    project_id = args.id
    if not args.variables:
        raise exc.CommandError(
            'Nothing to update... Please specify variables to set in the '
            'following format: "key=value". You may also specify variables to '
            'delete by key using the format: "key="'
        )
    adds, deletes = cliutils.variable_updates(args.variables)
    variables = cc.projects.get(project_id).variables
    variables.update(**adds)
    variables.delete(json=deletes)


@cliutils.arg('id',
              metavar='<project>',
              help='ID of the project.')
@cliutils.arg('variables', nargs=argparse.REMAINDER)
@cliutils.handle_shell_exception
def do_project_vars_delete(cc, args):
    """Delete variables for a project by key."""
    project_id = args.id
    if not args.variables:
        raise exc.CommandError(
            'Nothing to delete... Please specify variables to delete by '
            'listing the keys you wish to delete separated by spaces.'
        )
    deletes = cliutils.variable_deletes(args.variables)
    variables = cc.projects.get(project_id).variables
    variables.delete(json=deletes)
