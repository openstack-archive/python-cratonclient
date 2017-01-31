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


class VariablesMixin(crud.Resource):

    def __init__(self, manager, info, loaded=False):
        variables = info.get('variables')
        if variables is not None:
            var_mgr = VariablesManager(
                manager.session, manager.url, **manager.extra_request_kwargs)
            # TODO(jimbaker) this should be set above in the
            # construction of VariableManager itself, but for now it's
            # a workaround
            var_mgr.key = manager.key
            var_mgr.base_path = manager.base_path
            info['variables'] = Variables(
                var_mgr, info['variables'], resource=self, loaded=loaded)
        super(VariablesMixin, self).__init__(manager, info, loaded)


class Variables(crud.Resource):
    """An object for Variables."""

    def __init__(self, manager, info, resource=None, loaded=False):
        # follow resource convention and use _ prefix to hide from
        # __getattr__, __repr__
        self._resource = resource
        super(Variables, self).__init__(manager, info, loaded)

    def update(self, **kwargs):
        return self.manager.update(self._resource.id, **kwargs)

    def items(self):
        return sorted((k, v)
                      for k, v in self.__dict__.items()
                      if k[0] != '_' and k != 'manager')


class VariablesManager(crud.CRUDClient):
    """A manager of Variables."""

    resource_class = Variables

    def build_url(self, path_arguments=None):
        return super(VariablesManager, self).\
            build_url(path_arguments) + '/variables'
