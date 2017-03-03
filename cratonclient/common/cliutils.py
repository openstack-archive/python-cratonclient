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
"""Craton CLI helper classes and functions."""
import functools
import json
import os
import sys

from oslo_utils import encodeutils
from oslo_utils import strutils

from cratonclient import exceptions as exc


def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity.")
    ... def entity_create(args):
    ...     pass
    """
    def _decorator(func):
        """Decorator definition."""
        add_arg(func, *args, **kwargs)
        return func

    return _decorator


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""
    if not hasattr(func, 'arguments'):
        func.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in func.arguments:
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.arguments.insert(0, (args, kwargs))


def field_labels_from(attributes):
    """Generate a list of slightly more human readable field names.

    This takes the list of fields/attributes on the object and makes them
    easier to read.

    :param list attributes:
        The attribute names to convert. For example, ``["parent_id"]``.
    :returns:
        List of field names. For example ``["Parent Id"]``
    :rtype:
        list

    Example:

    >>> field_labels_from(["id", "name", "cloud_id"])
    ["Id", "Name", "Cloud Id"]
    """
    return [field.replace('_', ' ').title() for field in attributes]


def handle_shell_exception(function):
    """Generic error handler for shell methods."""
    @functools.wraps(function)
    def wrapper(cc, args):
        prop_map = {
            "vars": "variables"
        }
        try:
            function(cc, args)
        except exc.ClientException as client_exc:
            # NOTE(thomasem): All shell methods follow a similar pattern,
            # so we can parse this name to get intended parts for
            # messaging what went wrong to the end-user.
            # The pattern is "do_<resource>_(<prop>_)<verb>", like
            # do_project_show or do_project_vars_get, where <prop> is
            # not guaranteed to be there, but will afford support for
            # actions on some property of the resource.
            parsed = function.__name__.split('_')
            resource = parsed[1]
            verb = parsed[-1]
            prop = parsed[2] if len(parsed) > 3 else None
            msg = 'Failed to {}'.format(verb)
            if prop:
                # NOTE(thomasem): Prop would be something like "vars" in
                # "do_project_vars_get".
                msg = '{} {}'.format(msg, prop_map.get(prop))
            # NOTE(thomasem): Append resource and ClientException details
            # to error message.
            msg = '{} for {} {} due to "{}: {}"'.format(
                msg, resource, args.id, client_exc.__class__,
                encodeutils.exception_to_unicode(client_exc)
            )
            raise exc.CommandError(msg)

    return wrapper


def env(*args, **kwargs):
    """Return the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')


def convert_arg_value(v):
    """Convert different user inputs to normalized type."""
    # NOTE(thomasem): Handle case where one wants to escape this value
    # conversion using the format key='"value"'
    if v.startswith('"'):
        return v.strip('"')

    lower_v = v.lower()
    if strutils.is_int_like(v):
        return int(v)
    if strutils.is_valid_boolstr(lower_v):
        return strutils.bool_from_string(lower_v)
    if lower_v == 'null' or lower_v == 'none':
        return None
    try:
        return float(v)
    except ValueError:
        pass
    return v


def variable_updates(variables):
    """Derive list of expected variables for a resource and set them."""
    update_variables = {}
    delete_variables = set()
    for variable in variables:
        k, v = variable.split('=', 1)
        if v:
            update_variables[k] = convert_arg_value(v)
        else:
            delete_variables.add(k)
    if not sys.stdin.isatty():
        if update_variables or delete_variables:
            raise exc.CommandError("Cannot use variable settings from both "
                                   "stdin and command line arguments. Please "
                                   "choose one or the other.")
        update_variables = json.load(sys.stdin)
    return (update_variables, list(delete_variables))


def variable_deletes(variables):
    """Delete a list of variables (by key) from a resource."""
    if not sys.stdin.isatty():
        if variables:
            raise exc.CommandError("Cannot use variable settings from both "
                                   "stdin and command line arguments. Please "
                                   "choose one or the other.")
        delete_variables = json.load(sys.stdin)
    else:
        delete_variables = variables
    return delete_variables
