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
"""Regions manager code."""
from cratonclient import crud
from cratonclient.v1.variables import VariablesMixin


class Region(VariablesMixin):
    """Representation of a Region."""

    pass


class RegionManager(crud.CRUDClient):
    """A manager for regions."""

    key = 'region'
    base_path = '/regions'
    resource_class = Region
    project_id = 0

REGION_FIELDS = {
    'id': 'ID',
    'project_id': 'Project ID',
    'name': 'Name',
    'note': 'Note',
    'created_at': 'Created At',
    'updated_at': 'Updated At'
}
