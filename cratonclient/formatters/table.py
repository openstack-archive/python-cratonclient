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
"""Pretty-table formatter implementation for the craton CLI."""
from __future__ import print_function

import textwrap

from oslo_utils import encodeutils
import prettytable
import six

from cratonclient.common import cliutils
from cratonclient.formatters import base


class Formatter(base.Formatter):
    """Implementation of the default table-style formatter."""

    def after_init(self):
        """Set-up after initialization."""
        self.fields = []
        self.formatters = {}
        self.sortby_index = None
        self.mixed_case_fields = set([])
        self.field_labels = []
        self.dict_property = "Property"
        self.wrap = 0
        self.dict_value = "Value"

    def configure(self, fields=None, formatters=None, sortby_index=False,
                  mixed_case_fields=None, field_labels=None,
                  dict_property=None, dict_value=None, wrap=None):
        """Configure some of the settings used to print the tables.

        Parameters that configure list presentation:

        :param list fields:
            List of field names as strings.
        :param dict formatters:
            Mapping of field names to formatter functions that accept the
            resource.
        :param int sortby_index:
            The index of the field name in :param:`fields` to sort the table
            rows by. If ``None``, PrettyTable will not sort the items at all.
        :param list mixed_case_fields:
            List of field names also in :param:`fields` that are mixed case
            and need preprocessing prior to retrieving the attribute.
        :param list field_labels:
            List of field labels that need to match :param:`fields`.

        Parameters that configure the plain resource representation:

        :param str dict_property:
            The name of the first column.
        :param str dict_value:
            The name of the second column.
        :param int wrap:
            Length at which to wrap the second column.

        All of these may be specified, but will be ignored based on how the
        formatter is executed.
        """
        if fields is not None:
            self.fields = fields
        if field_labels is None:
            self.field_labels = cliutils.field_labels_from(self.fields)
        elif len(field_labels) != len(self.fields):
            raise ValueError(
                "Field labels list %(labels)s has different number "
                "of elements than fields list %(fields)s" %
                {'labels': field_labels, 'fields': fields}
            )
        else:
            self.field_labels = field_labels

        if formatters is not None:
            self.formatters = formatters

        if sortby_index is not False:
            try:
                sortby_index = int(sortby_index)
            except TypeError:
                if sortby_index is not None:
                    raise ValueError(
                        'sortby_index must be None or an integer'
                    )
            except ValueError:
                raise
            else:
                if self.field_labels and (
                        sortby_index < 0 or
                        sortby_index > len(self.field_labels)):
                    raise ValueError(
                        'sortby_index must be a non-negative number less '
                        'than {}'.format(len(self.field_labels))
                    )
            self.sortby_index = sortby_index

        if mixed_case_fields is not None:
            self.mixed_case_fields = set(mixed_case_fields)

        if dict_property is not None:
            self.dict_property = dict_property

        if dict_value is not None:
            self.dict_value = dict_value

        if wrap is not None:
            self.wrap = wrap

        return self

    def sortby_kwargs(self):
        """Generate the sortby keyword argument for PrettyTable."""
        if self.sortby_index is None:
            return {}
        return {'sortby': self.field_labels[self.sortby_index]}

    def build_table(self, field_labels, alignment='l'):
        """Create a PrettyTable instance based off of the labels."""
        table = prettytable.PrettyTable(field_labels)
        table.align = alignment
        return table

    def handle_generator(self, generator):
        """Handle a generator of resources."""
        sortby_kwargs = self.sortby_kwargs()
        table = self.build_table(self.field_labels)

        for resource in generator:
            resource_dict = resource.to_dict()
            row = []
            for field in self.fields:
                formatter = self.formatters.get(field)
                if formatter is not None:
                    data = formatter(resource)
                else:
                    if field in self.mixed_case_fields:
                        field_name = field.replace(' ', '_')
                    else:
                        field_name = field.lower().replace(' ', '_')
                    data = resource_dict.get(field_name, '')
                row.append(data)
            table.add_row(row)

        output = encodeutils.safe_encode(table.get_string(**sortby_kwargs))
        if six.PY3:
            output = output.decode()
        print(output)

    def handle_instance(self, instance):
        """Handle a single resource."""
        table = self.build_table([self.dict_property, self.dict_value])

        instance_dict = instance.to_dict()
        if self.fields:
            instance_dict = {field: instance_dict.get(field) for field
                             in self.fields}

        for key, value in sorted(instance_dict.items()):
            if isinstance(value, dict):
                value = six.text_type(value)
            if self.wrap > 0:
                value = textwrap.fill(six.text_type(value), self.wrap)

            if value and isinstance(value, six.string_types) and '\n' in value:
                lines = value.strip().split('\n')
                column1 = key
                for line in lines:
                    table.add_row([column1, line])
                    column1 = ''
            else:
                table.add_row([key, value])

        output = encodeutils.safe_encode(table.get_string())
        if six.PY3:
            output = output.decode()
        print(output)
