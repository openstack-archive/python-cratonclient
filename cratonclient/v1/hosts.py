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

    def list(self, region_id, **kwargs):
        """Retrieve the hosts in a specific region."""
        kwargs['region'] = str(region_id)
        return super(HostManager, self).list(**kwargs)


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
