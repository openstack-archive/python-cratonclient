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

    def __eq__(self, other):
        """Assess equality of Variable objects."""
        if isinstance(other, type(self)):
            return self.name == other.name and self.value == other.value
        return False

    def __repr__(self):
        """Return string representation of a Variable."""
        return '%(class)s(name=%(name)r, value=%(value)r)' % \
            {
                "class": self.__class__.__name__,
                "name": self.name,
                "value": self.value
            }


class Variables(MutableMapping):
    """Represents a dictionary of Variables."""

    _var_key = 'variables'

    def __init__(self, manager, info, loaded=False):
        """Instantiate a Variables dict.

        Converts each value to a Variable representation of the full key/value
        pair and assigns this mapping to self, as this extends the "dict"
        type.

        This class is intended to look like crud.Resource interface-wise, but
        it's unfortunately a hack to get around some limitations of
        crud.Resource, specifically how crud.Resource overlaying an API
        response onto a Python class can have variable keys conflicting with
        legitimate attributes of the class itself. Because this is supposed
        to be a dictionary-like thing, though, we don't wish to use the
        manager to make API calls when users are treating this like a dict.
        """
        self._manager = manager
        self._loaded = loaded
        self._variables_dict = {
            k: Variable(k, v)
            for (k, v) in info.get(self._var_key, dict()).items()
        }

    def __getitem__(self, key):
        """Get item from self._variables_dict."""
        return self._variables_dict[key]

    def __setitem__(self, key, value):
        """Set item in self._variables_dict."""
        self._variables_dict[key] = value

    def __delitem__(self, key):
        """Delete item from self._variables_dict."""
        del self._variables_dict[key]

    def __len__(self):
        """Get length of self._variables_dict."""
        return len(self._variables_dict)

    def __iter__(self):
        """Return iterator of self._variables_dict."""
        return iter(self._variables_dict)

    def __repr__(self):
        """Return string representation of Variables."""
        info = ", ".join("%s=%s" % (k, self._variables_dict[k]) for k, v in
                         self._variables_dict.items())
        return "<%s %s>" % (self.__class__.__name__, info)

    def to_dict(self):
        """Return this the original variables as a dict."""
        return {k: v.value for (k, v) in self._variables_dict.items()}


class VariableManager(crud.CRUDClient):
    """A CRUD manager for variables."""

    base_path = '/variables'
    resource_class = Variables

    def delete(self, *args, **kwargs):
        """Wrap crud.CRUDClient's delete to simplify for the variables.

        One can pass in a series of keys to delete, and this will pass the
        correct arguments to the crud.CRUDClient.delete function.

        .. code-block:: python

            >>> craton.hosts.get(1234).variables.delete('var-a', 'var-b')
            <Response [204]>
        """
        return super(VariableManager, self).delete(json=args, **kwargs)
