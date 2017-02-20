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
import prettytable
import six
import sys
import textwrap

from oslo_utils import encodeutils

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


def handle_shell_exception():
    """Generic error handler for shell methods."""
    def decorator(function):
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
                msg = '{} for {} {} due to "{}:{}"'.format(
                    msg, resource, args.id, client_exc.__class__,
                    str(client_exc))
                raise exc.CommandError(msg)

        return wrapper
    return decorator


def print_list(objs, fields, formatters=None, sortby_index=0,
               mixed_case_fields=None, field_labels=None):
    """Print a list or objects as a table, one row per object.

    :param objs: iterable of :class:`Resource`
    :param fields: attributes that correspond to columns, in order
    :param formatters: `dict` of callables for field formatting
    :param sortby_index: index of the field for sorting table rows
    :param mixed_case_fields: fields corresponding to object attributes that
        have mixed case names (e.g., 'serverId')
    :param field_labels: Labels to use in the heading of the table, default to
        fields.
    """
    formatters = formatters or {}
    mixed_case_fields = mixed_case_fields or []
    field_labels = field_labels or fields
    if len(field_labels) != len(fields):
        raise ValueError("Field labels list %(labels)s has different number "
                         "of elements than fields list %(fields)s",
                         {'labels': field_labels, 'fields': fields})

    if sortby_index is None:
        kwargs = {}
    else:
        kwargs = {'sortby': field_labels[sortby_index]}
    pt = prettytable.PrettyTable(field_labels)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                else:
                    field_name = field.lower().replace(' ', '_')
                data = getattr(o, field_name, '')
                row.append(data)
        pt.add_row(row)

    if six.PY3:
        print(encodeutils.safe_encode(pt.get_string(**kwargs)).decode())
    else:
        print(encodeutils.safe_encode(pt.get_string(**kwargs)))


def print_dict(dct, dict_property="Property", wrap=0, dict_value='Value',
               json_flag=False):
    """Print a `dict` as a table of two columns.

    :param dct: `dict` to print
    :param dict_property: name of the first column
    :param wrap: wrapping for the second column
    :param dict_value: header label for the value (second) column
    :param json_flag: print `dict` as JSON instead of table
    """
    if json_flag:
        print(json.dumps(dct, indent=4, separators=(',', ': ')))
        return
    pt = prettytable.PrettyTable([dict_property, dict_value])
    pt.align = 'l'
    for k, v in sorted(dct.items()):
        # convert dict to str to check length
        if isinstance(v, dict):
            v = six.text_type(v)
        if wrap > 0:
            v = textwrap.fill(six.text_type(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, six.string_types) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            pt.add_row([k, v])

    if six.PY3:
        print(encodeutils.safe_encode(pt.get_string()).decode())
    else:
        print(encodeutils.safe_encode(pt.get_string()))


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
    lower_v = v.lower()
    if lower_v == 'true':
        return True
    if lower_v == 'false':
        return False
    if lower_v == 'null' or lower_v == 'none':
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def set_variables(resource, args):
    """Derive list of expected variables for a resource and set them."""
    update_variables = {}
    delete_variables = set()
    for variable in args.variables:
        k, v = variable.split('=', 1)
        if v:
            update_variables[k] = convert_arg_value(v)
        else:
            delete_variables.add(k)
    if not sys.stdin.isatty():
        if update_variables or delete_variables:
            raise Exception("FIXME cannot set on command line as well!")
        update_variables = json.load(sys.stdin)
    if update_variables:
        resource.set_variables(**update_variables)
    if delete_variables:
        resource.delete_variables(*delete_variables)


def delete_variables(resource, args):
    """Delete a list of variables (by key) from a resource."""
    if not sys.stdin.isatty():
        if args.variables:
            raise Exception("FIXME cannot delete on command line as well!")
        delete_variables = json.load(sys.stdin)
    else:
        delete_variables = args.variables
    resource.variables.delete(*delete_variables)
