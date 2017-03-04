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
from cratonclient.v1 import variables


class Cell(crud.Resource):
    """Representation of a Region."""

    subresource_managers = {
        'variables': variables.VariableManager,
    }


class CellManager(crud.CRUDClient):
    """A manager for cells."""

    key = 'cell'
    base_path = '/cells'
    resource_class = Cell
