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
"""Variables resource and resource manager."""
from cratonclient import crud


class ResourceWithVariables(crud.Resource):
    """Base class for resources that have variables support."""

    def __init__(self, manager, info, loaded=False):
        """Handle "loaded" logic and wrap variables in Variables class.

        Handle some logic for setting "loaded" to indicate to lazy-loader
        whether we need to load the variables.
        """
        variables = info.get('variables')
        if variables is None:
            # NOTE(thomasem): Variables being None instead of just {} indicates
            # variables haven't been loaded yet. So, force loaded to False
            # and set variables to an empty dict. One would default variables
            # to {} when looking up "variables" in info, except we need to know
            # whether it actually is None in order to set loaded to the
            # appropriate value.
            variables = {}
            loaded = False

        info['variables'] = Variables(
            manager=VariablesManager(manager),
            info=variables,
            resource=self,
            loaded=loaded
        )
        super(ResourceWithVariables, self).__init__(manager, info, loaded)


class Variables(crud.Resource):
    """An object for Variables."""

    def __init__(self, manager, info, resource=None, loaded=False):
        """Instantiate Variables."""
        # NOTE(jimbaker): follow resource convention and use _ prefix to hide
        # from __getattr__, __repr__
        self._resource = resource
        super(Variables, self).__init__(manager, info, loaded)

    @property
    def id(self):
        """Return ID of resource."""
        return self._resource.id

    def update(self, **kwargs):
        """Update variables for resource."""
        return self.manager.update(self._resource.id, **kwargs)

    def delete(self, *keys):
        """Delete the desired variables specified by keys."""
        url = self.manager.build_url(
            {self.manager.key + '_id': self._resource.id})
        response = self.manager.session.delete(url, json=keys)
        return 200 <= response.status_code < 300

    def items(self):
        """Return sorted tuples of Variables."""
        return sorted((k, v)
                      for k, v in self.__dict__.items()
                      if self.is_resource_property(k))


class VariablesManager(crud.CRUDClient):
    """A manager of Variables."""

    resource_class = Variables

    def __init__(self, manager):
        """Instantiate VariablesManager."""
        self.key = manager.key
        self.base_path = manager.base_path
        super(VariablesManager, self).__init__(
            manager.session, manager.url)

    def build_url(self, path_arguments=None):
        """Wrap parent class's build_url with standard '/variables' suffix.

        This allows us to utilize a different URL when interacting with a
        resource's variables.
        """
        return super(VariablesManager, self).\
            build_url(path_arguments) + '/variables'
