====================================
 Python API Reference Documentation
====================================

This chapter of python-cratonclient's documentation focuses entirely on
the API of the different objects involved in the use of cratonclient's
Python API.


Version-less Objects
====================

.. autoclass:: cratonclient.session.Session


v1 API Documentation
====================

.. autoclass:: cratonclient.v1.client.Client

.. NOTE(sigmavirus24): These could all use the regular ``.. class`` directive
   instead and document each method and attribute individually. This is a good
   start instead of trying to document everything all at once.

Cells
-----

.. autoclass:: cratonclient.v1.cells.Cell
    :members: get, delete, human_id, is_loaded

.. autoclass:: cratonclient.v1.cells.CellManager
    :members: create, delete, get, list, update

Clouds
------

.. autoclass:: cratonclient.v1.clouds.Cloud
    :members: get, delete, human_id, is_loaded

.. autoclass:: cratonclient.v1.clouds.CloudManager
    :members: create, delete, get, list, update

Devices
-------

.. autoclass:: cratonclient.v1.devices.Device
    :members: get, delete, human_id, is_loaded

.. autoclass:: cratonclient.v1.devices.DeviceManager
    :members: list

Hosts
-----

.. autoclass:: cratonclient.v1.hosts.Host
    :members: get, delete, human_id, is_loaded

.. autoclass:: cratonclient.v1.hosts.HostManager
    :members: create, delete, get, list, update

Projects
--------

.. autoclass:: cratonclient.v1.projects.Project
    :members: get, delete, human_id, is_loaded

.. autoclass:: cratonclient.v1.projects.ProjectManager
    :members: create, delete, get, list, update

Regions
-------

.. autoclass:: cratonclient.v1.regions.Region
    :members: get, delete, human_id, is_loaded

.. autoclass:: cratonclient.v1.regions.RegionManager
    :members: create, delete, get, list, update

Variables
---------

.. autoclass:: cratonclient.v1.variables.Variable

.. autoclass:: cratonclient.v1.variables.Variables

.. autoclass:: cratonclient.v1.variables.VariableManager
    :members: create, delete, get, list, update


Authentication Helpers
======================

.. autofunction:: cratonclient.auth.craton_auth

.. autofunction:: cratonclient.auth.keystone_auth
