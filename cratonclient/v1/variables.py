# -*- coding: utf-8 -*-

"""Variables resource and resource manager."""
from cratonclient import crud


class VariablesMixin(crud.Resource):
    
    def __init__(self, manager, info, loaded=False):
        try:
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
                    var_mgr, info['variables'], host=self, loaded=loaded)
        except AttributeError:
            # TODO(jimbaker) currently we can get multiple instances of a host, etc loaded
            pass
        super().__init__(manager, info, loaded)


class Variables(crud.Resource):
    """An object for Variables."""

    def __init__(self, manager, info, host=None, loaded=False):
        # follow resource convention and use _ prefix to hide from
        # __getattr__, __repr__
        self._host = host
        super().__init__(manager, info, loaded)

    def update(self, **kwargs):
        return self.manager.update(self._host.id, **kwargs)

    def items(self):
        return sorted((k, v)
                      for k, v in self.__dict__.items()
                      if k[0] != '_' and k != 'manager')


class VariablesManager(crud.CRUDClient):
    """A manager of Variables."""

    key = 'host'
    base_path = '/hosts'
    resource_class = Variables

    def build_url(self, path_arguments=None):
        return super().build_url(path_arguments) + '/variables'
