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

    def __init__(self, manager, info, loaded=False):
        variables = info.get('variables')
        if variables is not None:
            var_mgr = VariablesManager(manager)
            info['variables'] = Variables(
                var_mgr, info['variables'], resource=self, loaded=loaded)
        else:
            var_mgr = VariablesManager(manager)
            info['variables'] = Variables(
                var_mgr, {}, resource=self, loaded=False)
        super(ResourceWithVariables, self).__init__(manager, info, loaded)


class Variables(crud.Resource):
    """An object for Variables."""

    def __init__(self, manager, info, resource=None, loaded=False):
        # follow resource convention and use _ prefix to hide from
        # __getattr__, __repr__
        self._resource = resource
        super(Variables, self).__init__(manager, info, loaded)

    @property
    def id(self):
        return self._resource.id

    def update(self, **kwargs):
        return self.manager.update(self._resource.id, **kwargs)

    def delete(self, *keys):
        """Delete the desired variables specified by keys."""
        url = self.manager.build_url(
            {self.manager.key + '_id': self._resource.id})
        response = self.manager.session.delete(url, json=keys)
        return 200 <= response.status_code < 300

    def items(self):
        return sorted((k, v)
                      for k, v in self.__dict__.items()
                      if k[0] != '_' and k != 'manager')


class VariablesManager(crud.CRUDClient):
    """A manager of Variables."""

    resource_class = Variables

    def __init__(self, manager):
        self.key = manager.key
        self.base_path = manager.base_path
        super(VariablesManager, self).__init__(
            manager.session, manager.url)

    def build_url(self, path_arguments=None):
        return super(VariablesManager, self).\
            build_url(path_arguments) + '/variables'
