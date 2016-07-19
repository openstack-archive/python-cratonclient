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
import os
import prettytable
import six

from oslo_utils import encodeutils


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


def env(*args, **kwargs):
    """Return the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')
