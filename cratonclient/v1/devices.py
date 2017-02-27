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
"""Devices manager code."""
from cratonclient import crud


class Device(crud.Resource):
    """Representation of a Device."""

    pass


class DeviceManager(crud.CRUDClient):
    """A manager for devices."""

    key = 'device'
    base_path = '/devices'
    resource_class = Device

DEVICE_FIELDS = {
    'id': 'ID',
    'project_id': 'Project ID',
    'cloud_id': 'Cloud ID',
    'region_id': 'Region ID',
    'cell_id': 'Cell ID',
    'parent_id': 'Parent ID',
    'name': 'Name',
    'ip_address': 'IP Address',
    'device_type': 'Device Type',
    'note': 'Note',
    'created_at': 'Created At',
    'updated_at': 'Updated At'
}
