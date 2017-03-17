======================
 Using the Clouds API
======================

Here we will assume that we already have a
:class:`~cratonclient.client.Client` instance configured with the appropriate
authentication method (as demonstrated in :ref:`usage-auth`).

Listing Clouds
--------------

The Clouds API implements pagination. This means that by default, it does not
return all clouds known to Craton. To ignore page limits and offsets, we can
allow cratonclient to do handle pagination for us:

.. code-block:: python

   for cloud in craton.clouds.list():
       print_cloud_info(cloud)

By default :meth:`~cratonclient.v1.clouds.CloudsManager.list` will handle
pagination for you. If, instead, you want to handle it yourself you will want
to do something akin to:

.. code-block:: python

    first_page_of_clouds = list(craton.clouds.list(autopaginate=False))
    marker_id = first_page_of_clouds[-1].id
    second_page_of_clouds = list(craton.clouds.list(
        autopaginate=False,
        marker=marker_id,
    ))
    marker_id = second_page_of_clouds[-1].id
    third_page_of_clouds = list(craton.clouds.list(
        autopaginate=False,
        marker=marker_id,
    ))
    # etc.

A more realistic example, however, might look like this:

.. code-block:: python

    clouds_list = None
    marker = None
    while clouds_list and clouds_list is not None:
        clouds_list = list(craton.clouds.list(
            marker=marker,
            autopaginate=False,
        ))
        # do something with clouds_list
        if clouds_list:
            marker = clouds_list[-1].id

This will have the effect of stopping the while loop when you eventually
receive an empty list from ``craton.clouds.list(...)``.

Creating Clouds
---------------

Clouds are the top-level item in Craton. To create a cloud, the only required
item is a ``name`` for the cloud. This must be unique among clouds in the same
project.

.. code-block:: python

    cloud = craton.clouds.create(
        name='my-cloud-0',
        note='This is my cloud, there are many like it, but this is mine.',
        variables={
            'some-var': 'some-var-value',
        },
    )

Retrieving a Specific Cloud
---------------------------

Clouds can be retrieved by id.

.. code-block:: python

    cloud = craton.clouds.get(1)

Using a Cloud's Variables
-------------------------

Once we have a cloud we can introspect its variables like so:

.. code-block:: python

    cloud = craton.clouds.get(cloud_id)
    cloud_vars = cloud.variables.get()

To update them:

.. code-block:: python

    updated_vars = {
        'var-a': 'new-var-a',
        'var-b': 'new-var-b',
        'updated-var': 'updated value',
    }
    cloud.variables.update(**updated_vars)

To delete them:

.. code-block:: python

    cloud.variables.delete('var-a', 'var-b', 'updated-var')

Updating a Cloud
----------------

We can update a cloud's attributes (but not its variables) like so:

.. code-block:: python

    craton.clouds.update(
        cloud_id,
        name='new name',
        note='Updated note.',
    )

Most attributes that you can specify on creation can also be specified for
updating the cloud as well.

Deleting a Cloud
----------------

We can delete with only its id:

.. code-block:: python

    craton.clouds.delete(cloud_id)
