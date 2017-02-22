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


HOST_FIELDS = {
    'id': 'ID',
    'name': 'Name',
    'device_type': 'Device Type',
    'project_id': 'Project ID',
    'cloud_id': 'Cloud ID',
    'region_id': 'Region ID',
    'cell_id': 'Cell ID',
    'ip_address': 'IP Address',
    'active': 'Active',
    'note': 'Note',
    'created_at': 'Created At',
    'updated_at': 'Updated At',
    'labels': 'Labels',
}
