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
"""Clouds manager code."""
from cratonclient import crud
from cratonclient.v1.variables import ResourceWithVariables


class Cloud(ResourceWithVariables):
    """Representation of a Cloud."""

    pass


class CloudManager(crud.CRUDClient):
    """A manager for clouds."""

    key = 'cloud'
    base_path = '/clouds'
    resource_class = Cloud

CLOUD_FIELDS = {
    'id': 'ID',
    'project_id': 'Project ID',
    'name': 'Name',
    'note': 'Note',
    'created_at': 'Created At',
    'updated_at': 'Updated At'
}
