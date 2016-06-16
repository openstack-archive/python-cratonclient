"""Hosts resource and resource manager."""
from cratonclient import crud


class Host(crud.Resource):
    """Representation of a Host."""

    pass


class HostManager(crud.CRUDClient):
    """A manager for hosts."""

    key = 'host'
    base_path = '/hosts'
    resource_class = Host

    def list(self, project_id, **kwargs):
        """Retrieve the hosts in a specific region."""
        kwargs['project'] = str(project_id)
        super(HostManager, self).list(**kwargs)
