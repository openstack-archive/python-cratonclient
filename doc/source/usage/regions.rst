=======================
 Using the Regions API
=======================

Here we will assume that we already have a
:class:`~cratonclient.client.Client` instance configured with the appropriate
authentication method (as demonstrated in :ref:`usage-auth`).

Listing Regions
---------------

The Regions API implements pagination. This means that by default, it does not
return all regions known to Craton. To ignore page limits and offsets, we can
allow cratonclient to do handle pagination for us:

.. code-block:: python

   for region in craton.regions.list():
       print_region_info(region)

By default :meth:`~cratonclient.v1.regions.RegionsManager.list` will handle
pagination for you. If, instead, you want to handle it yourself you will want
to do something akin to:

.. code-block:: python

    first_page_of_regions = list(craton.regions.list(autopaginate=False))
    marker_id = first_page_of_regions[-1].id
    second_page_of_regions = list(craton.regions.list(
        autopaginate=False,
        marker=marker_id,
    ))
    marker_id = second_page_of_regions[-1].id
    third_page_of_regions = list(craton.regions.list(
        autopaginate=False,
        marker=marker_id,
    ))
    # etc.

A more realistic example, however, might look like this:

.. code-block:: python

    regions_list = None
    marker = None
    while regions_list and regions_list is not None:
        regions_list = list(craton.regions.list(
            marker=marker,
            autopaginate=False,
        ))
        # do something with regions_list
        if regions_list:
            marker = regions_list[-1].id

This will have the effect of stopping the while loop when you eventually
receive an empty list from ``craton.regions.list(...)``.

Creating Regions
----------------

Regions are required to be part of a Cloud in Craton. To create a region, the
only required items are a ``name`` for the region and the ID of the cloud it
belongs to. The name must be unique among regions in the same project.

.. code-block:: python

    region = craton.regions.create(
        name='my-region-0',
        cloud_id=cloud_id,
        note='This is my region, there are many like it, but this is mine.',
        variables={
            'some-var': 'some-var-value',
        },
    )

Retrieving a Specific Region
----------------------------

Regions can be retrieved by id.

.. code-block:: python

    region = craton.regions.get(1)

Using a Region's Variables
--------------------------

Once we have a region we can introspect its variables like so:

.. code-block:: python

    region = craton.regions.get(region_id)
    region_vars = region.variables.get()

To update them:

.. code-block:: python

    updated_vars = {
        'var-a': 'new-var-a',
        'var-b': 'new-var-b',
        'updated-var': 'updated value',
    }
    region.variables.update(**updated_vars)

To delete them:

.. code-block:: python

    region.variables.delete('var-a', 'var-b', 'updated-var')

Updating a Region
-----------------

We can update a region's attributes (but not its variables) like so:

.. code-block:: python

    craton.regions.update(
        region_id,
        name='new name',
        note='Updated note.',
    )

Most attributes that you can specify on creation can also be specified for
updating the region as well.

Deleting a Region
-----------------

We can delete with only its id:

.. code-block:: python

    craton.regions.delete(region_id)
