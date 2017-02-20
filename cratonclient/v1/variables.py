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
from cratonclient import crud


class Variable(object):
    """Represents a Craton variable key/value pair."""

    def __init__(self, name, value):
        """Instantiate key/value pair."""
        self.name = name
        self.value = value


class Variables(dict):
    """Represents a dictionary of Variables."""
    def __init__(self, manager, info, loaded=False):
        for (k, v) in self._to_variables_dict(info['variables']).items():
            self[k] = v

    def _to_variables_dict(self, variables):
        wrapped = {}
        for (k, v) in variables.items():
            if isinstance(v, dict):
                v = self._to_variables_dict(v)
            wrapped[k] = Variable(k, v)
        return wrapped

    def to_dict(self, value=None):
        unwrapped = {}
        value = value or self
        for (k, v) in value.items():
            v = v.value
            if isinstance(v, dict):
                v = self.to_dict(v)
            unwrapped[k] = v
        return unwrapped


class VariableManager(crud.CRUDClient):
    """A CRUD manager for variables."""

    key = 'variables'
    base_path = '/variables'
    # NOTE(thomasem): Unfortunate byproduct of how flexible variables must be,
    # we cannot reliably use crud.Resource to embody a dict with so few
    # guarantees around what keys may be in use. For example, if I were to use
    # some crud.Resource derivative here, and I get a variable with a name that
    # matches, say, "manager", there's going to be a conflict as that's an
    # actual attribute of the cloud pointing to the CRUDClient manager for that
    # resource. So, we will just make a dict instead.
    resource_class = Variables
