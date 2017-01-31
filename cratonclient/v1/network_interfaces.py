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


class NetworkInterfaces(crud.Resource):
    """Representation of a Network Interfaces."""

    pass


class NetworkInterfaceManager(crud.CRUDClient):
    """A manager for network devices."""

    key = 'network_interface'
    base_path = '/network-interfaces'
    resource_class = NetworkInterfaces


NETWORK_INTERFACE_FIELDS = {
    'id': 'ID',
    'region_id': 'Region ID',
    'cell_id': 'Cell ID',
    'project_id': 'Project ID',
    'name': 'Name',
    'device_id': 'Device Id',
    'interface_type': 'Interface Type',
    'ip_address': 'IP Address',
    'network_id': 'Network ID',
    'vlan_id': 'VLAN Type',
    'vlan': 'VLAN',
    'port': 'Port',
    'duplex': 'Duplex',
    'speed': 'Speed',
    'link': 'Link',
    'cdp': 'CDP',
    'security': 'Security',
    'created_at': 'Created At',
    'update_at': 'Updated At'
}
