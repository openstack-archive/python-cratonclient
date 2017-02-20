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
        variables = info.get('variables', {})
        for (k, v) in self._to_variables_dict(variables).items():
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
    resource_class = Variables
