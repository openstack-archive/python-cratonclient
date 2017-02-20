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
"""Variables manager code."""
from collections import MutableMapping
from cratonclient import crud


class Variable(object):
    """Represents a Craton variable key/value pair."""

    def __init__(self, name, value):
        """Instantiate key/value pair."""
        self.name = name
        self.value = value


class Variables(MutableMapping):
    """Represents a dictionary of Variables."""
    def __init__(self, manager, info, loaded=False):
        """Instantiate a Variables dict.

        Converts each value to a Variable representation of the full key/value
        pair and assigns this mapping to self, as this extends the "dict"
        type.
        """
        self._original = info.get('variables', dict())
        self._variables_dict = self._to_variables_dict(self._original)

    def __getitem__(self, key):
        return self._variables_dict[key]

    def __setitem__(self, key, value):
        self._variables_dict[key] = value

    def __delitem__(self, key):
        del self._variables_dict[key]

    def __len__(self):
        return len(self._variables_dict)

    def __iter__(self):
        return iter(self._variables_dict)

    def _to_variables_dict(self, variables):
        """Produce a Variables dict

        For example:

        Take
        {
            "foo": "bar",
            "zoo": {
                "baz": "zab"
            }
        }

        and turn it into
        {
            "foo": Variable(name="foo", value="bar"),
            "zoo": Variable(
                name="zoo", value={
                    "baz": Variable(name="baz", value="zab")
                }
            )
        }

        """
        wrapped = {}
        for (k, v) in variables.items():
            if isinstance(v, dict):
                v = self._to_variables_dict(v)
            wrapped[k] = Variable(k, v)
        return wrapped

    def to_dict(self):
        """Return this the original variables as a dict."""
        return self._original


class VariableManager(crud.CRUDClient):
    """A CRUD manager for variables."""

    base_path = '/variables'
    resource_class = Variables
