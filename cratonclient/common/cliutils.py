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


def env(*args, **kwargs):
    """Return the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')
