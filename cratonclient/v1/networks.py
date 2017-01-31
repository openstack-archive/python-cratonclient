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
"""Networks manager code."""
from cratonclient import crud


class Networks(crud.Resource):
    """Representation of a Network."""

    pass


class NetworksManager(crud.CRUDClient):
    """A manager for networks."""

    key = 'network'
    base_path = '/networks'
    resource_class = Networks


NETWORKS_FIELDS = {
    'id': 'ID',
    'region_id': 'Region ID',
    'cell_id': 'Cell ID',
    'project_id': 'Project ID',
    'name': 'Name',
    'cidr': 'CIDR',
    'gateway': 'Gateway',
    'netmask': 'Netmask',
    'ip_block_type': 'IP Block Type',
    'nss': 'NSS',
    'created_at': 'Created At',
    'update_at': 'Updated At'
}
