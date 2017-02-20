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
"""Base class implementation for formatting plugins."""
from cratonclient import crud
from cratonclient.v1 import variables


class Formatter(object):
    """Class that defines the formatter interface.

    Instead of having to override and call up to this class's ``__init__``
    method, we also provide an ``after_init`` method that can be implemented
    to extend what happens on initialization.

    .. attribute:: args

        Parsed command-line arguments stored as an instance of
        :class:`argparse.Namespace`.

    """

    def __init__(self, parsed_args):
        """Instantiate our formatter with the parsed CLI arguments.

        :param parsed_args:
            The CLI arguments parsed by :mod:`argparse`.
        :type parsed_args:
            argparse.Namespace
        """
        self.args = parsed_args
        self.after_init()

    def after_init(self):
        """Initialize the object further after ``__init__``."""
        pass

    def configure(self, *args, **kwargs):
        """Optional configuration of the plugin after instantiation."""
        return self

    def handle(self, item_to_format):
        """Handle a returned item from the cratonclient API.

        cratonclient's API produces both single Resource objects as well as
        generators of those objects. This method should be capable of handling
        both.

        Based on the type, this will either call ``handle_generator`` or
        ``handle_instance``. Subclasses must implement both of those methods.

        :returns:
            None
        :rtype:
            None
        :raises ValueError:
            If the item provided is not a subclass of
            :class:`~cratonclient.crud.Resource` or an iterable class then
            we will not know how to handle it. In that case, we will raise a
            ValueError.
        """
        if type(item_to_format) in [crud.Resource, variables.Variables]:
            self.handle_instance(item_to_format)
            return

        try:
            self.handle_generator(item_to_format)
        except TypeError as err:
            raise ValueError(
                "Expected an iterable object but instead received something "
                "of type: %s. Received a TypeError: %s" % (
                    type(item_to_format),
                    err
                )
            )

    def handle_instance(self, instance):
        """Format and print the instance provided.

        :param instance:
            The instance retrieved from the API that needs to be formatted.
        :type instance:
            cratonclient.crud.Resource
        """
        raise NotImplementedError(
            "A formatter plugin subclassed Formatter but did not implement"
            " the handle_instance method."
        )

    def handle_generator(self, generator):
        """Format and print the instance provided.

        :param generator:
            The generator retrieved from the API whose items need to be
            formatted.
        """
        raise NotImplementedError(
            "A formatter plugin subclassed Formatter but did not implement"
            " the handle_generator method."
        )
