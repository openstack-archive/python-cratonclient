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

    def get(self, host_id):
        """Get a host.

        .. code-block:: python

        >>> from cratonclient.v1 import client
        >>> from cratonclient import session
        >>> session = session.Session(
        ...     username='demo',
        ...     token='password',
        ...     project_id=1
        ... )
        >>> client = client.Client(session, 'http://example.com')
        >>> created_host = client.hosts.create(
        ...     name='test',
        ...     project_id=1,
        ...     region_id=1,
        ...     ip_address='127.0.0.1',
        ...     device_type="type"
        ... )
        >>> gotten_host= client.hosts.get(host.id)
        """
        return super(HostManager, self).get(host_id=host_id)

    def create(self, name, project_id, region_id, ip_address,
               device_type, active=True, **kwargs):
        """Create a host.

        .. code-block:: python

        >>> from cratonclient.v1 import client
        >>> from cratonclient import session
        >>> session = session.Session(
        ...     username='demo',
        ...     token='password',
        ...     project_id=1
        ... )
        >>> client = client.Client(session, 'http://example.com')
        >>> client.hosts.create(
        ...     name='test',
        ...     project_id=1,
        ...     region_id=1,
        ...     ip_address='127.0.0.1',
        ...     device_type="type"
        ... )
        """
        return super(HostManager, self).create(name=name,
                                               project_id=project_id,
                                               region_id=region_id,
                                               ip_address=ip_address,
                                               device_type=device_type,
                                               active=active,
                                               **kwargs)

    def list(self, project_id, **kwargs):
        """Retrieve the hosts in a specific region."""
        kwargs['project'] = str(project_id)
        return super(HostManager, self).list(**kwargs)

    def update(self, host_id, **kwargs):
        """Update a host.

        .. code-block:: python

        >>> from cratonclient.v1 import client
        >>> from cratonclient import session
        >>> session = session.Session(
        ...     username='demo',
        ...     token='password',
        ...     project_id=1
        ... )
        >>> client = client.Client(session, 'http://example.com')
        >>> host = client.hosts.create(
        ...     name='test',
        ...     project_id=1,
        ...     region_id=1,
        ...     ip_address='127.0.0.1',
        ...     device_type="type"
        ... )
        >>> client.hosts.update(host.id, region_id=2)
        """
        return super(HostManager, self).update(host_id=host_id, **kwargs)

    def delete(self, host_id):
        """Delete a host.

        .. code-block:: python

        >>> from cratonclient.v1 import client
        >>> from cratonclient import session
        >>> session = session.Session(
        ...     username='demo',
        ...     token='password',
        ...     project_id=1
        ... )
        >>> client = client.Client(session, 'http://example.com')
        >>> host = client.hosts.create(
        ...     name='test',
        ...     project_id=1,
        ...     region_id=1,
        ...     ip_address='127.0.0.1',
        ...     device_type="type"
        ... )
        >>> client.hosts.delete(host.id)
        """
        super(HostManager, self).delete(host_id=host_id)

HOST_FIELDS = {
    'id': 'ID',
    'name': 'Name',
    'type': 'Type',
    'project_id': 'Project ID',
    'region_id': 'Region ID',
    'cell_id': 'Cell ID',
    'ip_address': 'IP Address',
    'active': 'Active',
    'note': 'Note',
    'access_secret_id': "Access Secret ID",
    'created_at': 'Created At',
    'update_at': 'Updated At'
}
