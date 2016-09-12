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
    region_id = 0

    def __init__(self, region_id, session, url):
        """Initialize our HostManager object with region, session and url."""
        super(HostManager, self).__init__(session, url)
        self.region_id = region_id

    def list(self, **kwargs):
        """Retrieve the hosts in a specific region."""
        kwargs['region_id'] = self.region_id
        return super(HostManager, self).list(**kwargs)

    def create(self, **kwargs):
        """Create a host in a specific region."""
        kwargs['region_id'] = self.region_id
        return super(HostManager, self).create(**kwargs)


HOST_FIELDS = {
    'id': 'ID',
    'name': 'Name',
    'device_type': 'Device Type',
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
