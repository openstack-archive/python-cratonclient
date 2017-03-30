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
"""JSON formatter implementation for the craton CLI."""
from __future__ import print_function

import json

from cratonclient.formatters import base


class Formatter(base.Formatter):
    """JSON output formatter for the CLI."""

    def after_init(self):
        """Set-up our defaults.

        At some point in the future, we may allow people to configure this via
        the CLI.
        """
        self.indent = 4
        self.sort_keys = True
        self.fields = []

    def configure(self, fields=None, **kwargs):
        """Configure some of the settings used to output JSON.

        Parameters that configure JSON presentation:

        :param list fields:
            List of field names as strings.
        """
        if fields is not None:
            self.fields = fields

        return self

    def format(self, dictionary):
        """Return the dictionary as a JSON string."""
        return json.dumps(
            dictionary,
            sort_keys=self.sort_keys,
            indent=self.indent,
        )

    def handle_instance(self, instance):
        """Print the JSON representation of a single instance."""
        instance_dict = instance.to_dict()
        if self.fields:
            instance_dict = {field: instance_dict.get(field) for field
                             in self.fields}
        print(self.format(instance_dict))

    def handle_generator(self, generator):
        """Print the JSON representation of a collection."""
        # NOTE(sigmavirus24): This is tricky logic that is caused by the JSON
        # specification's intolerance for trailing commas.
        try:
            instance = next(generator)
        except StopIteration:
            # If there is nothing in the generator, we should just print an
            # empty Array and then exit immediately.
            print('[]')
            return

        # Otherwise, let's print our opening bracket to start our Array
        # formatting.
        print('[', end='')
        while True:
            instance_dict = instance.to_dict()
            if self.fields:
                instance_dict = {field: instance_dict.get(field) for field
                                 in self.fields}
            print(self.format(instance_dict), end='')
            # After printing our instance as a JSON object, we need to
            # decide if we have another object to print. If we do have
            # another object to print, we need to print a comma to separate
            # our previous object and our next one. If we don't, we exit our
            # loop to print our closing Array bracket.
            try:
                instance = next(generator)
            except StopIteration:
                break
            else:
                print(', ', end='')
        print(']')
