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
"""Network Devices manager code."""
from cratonclient import crud


class NetworkDevices(crud.Resource):
    """Representation of a Network Devices."""

    pass


class NetworkDevicesManager(crud.CRUDClient):
    """A manager for network devices."""

    key = 'network_device'
    base_path = '/network-devices'
    resource_class = NetworkDevices


NETWORK_DEVICE_FIELDS = {
    'id': 'ID',
    'region_id': 'Region ID',
    'cell_id': 'Cell ID',
    'project_id': 'Project ID',
    'name': 'Name',
    'model_name': 'Model',
    'os_version': 'OS Version',
    'vlans': 'Vlans',
    'active': 'Active',
    'device_type': 'Device Type',
    'ip_address': 'IP Adress',
    'created_at': 'Created At',
    'update_at': 'Updated At'
}
