=======================
 Using the Devices API
=======================

Here we will assume that we already have a
:class:`~cratonclient.client.Client` instance configured with the appropriate
authentication method (as demonstrated in :ref:`usage-auth`).

.. note::

    The Devices API is quite unlike other API endpoints presently in craton.
    At the moment, it returns both hosts and network devices. It concatenates
    the two lists in an indeterminate manner. On one invocation, you may
    receive the hosts first and then the network devices, on another you may
    receive them in the alternate order. If more items are returned in these
    listings, then the number of different orderings will only increase
    factorially.

Listing Devices
---------------

The Devices API implements pagination. This means that by default, it does not
return all devices known to Craton. To ignore page limits and offsets, we can
allow cratonclient to do handle pagination for us:

.. code-block:: python

   for device in craton.devices.list():
       print_device_info(device)

By default :meth:`~cratonclient.v1.devices.DevicesManager.list` will handle
pagination for you.
