===========================
 Communicating with Craton
===========================

Now that you've configured your authentication method, you can interact with
your ``craton`` object like so:

.. code-block:: python

    for region in craton.regions.list():
        print('Region {} contains:'.format(region.name))
        for host in craton.hosts.list(region_id=region.id):
            print('    {}'.format(host.name))


The Craton API has the following resources:

- Cells

- Clouds

- Devices

- Hosts

- Network Devices

- Network Interfaces

- Networks

- Projects

- Regions

- Users

Of these:

- Cells

- Clouds

- Hosts

- Projects

- Regions

Are implemented.
