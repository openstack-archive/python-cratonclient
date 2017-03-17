=====================
 Using the Cells API
=====================

Here we will assume that we already have a
:class:`~cratonclient.client.Client` instance configured with the appropriate
authentication method (as demonstrated in :ref:`usage-auth`).

Listing Cells
-------------

The Cells API implements pagination. This means that by default, it does not
return all cells known to Craton. To ignore page limits and offsets, we can
allow cratonclient to do handle pagination for us:

.. code-block:: python

   for cell in craton.cells.list():
       print_cell_info(cell)

By default :meth:`~cratonclient.v1.cells.CellManager.list` will handle
pagination for you. If, instead, you want to handle it yourself you will want
to do something akin to:

.. code-block:: python

    first_page_of_cells = list(craton.cells.list(autopaginate=False))
    marker_id = first_page_of_cells[-1].id
    second_page_of_cells = list(craton.cells.list(
        autopaginate=False,
        marker=marker_id,
    ))
    marker_id = second_page_of_cells[-1].id
    third_page_of_cells = list(craton.cells.list(
        autopaginate=False,
        marker=marker_id,
    ))
    # etc.

A more realistic example, however, might look like this:

.. code-block:: python

    cells_list = None
    marker = None
    while cells_list and cells_list is not None:
        cells_list = list(craton.cells.list(
            marker=marker,
            autopaginate=False,
        ))
        # do something with cells_list
        if cells_list:
            marker = cells_list[-1].id

This will have the effect of stopping the while loop when you eventually
receive an empty list from ``craton.cells.list(...)``.

Creating Cells
--------------

Cells live below a Region in Craton. To create a cell, the only required items
are a ``name`` for the cell, a cloud ID, and a region ID. The name must be
unique among cells in the same project.

.. code-block:: python

    cell = craton.cells.create(
        name='my-cell-0',
        cloud_id=cloud_id,
        region_id=region_id,
        note='This is my cell, there are many like it, but this is mine.',
        variables={
            'some-var': 'some-var-value',
        },
    )

Retrieving a Specific Cell
--------------------------

Cells can be retrieved by id.

.. code-block:: python

    cell = craton.cells.get(1)

Using a Cell's Variables
-------------------------

Once we have a cell we can introspect its variables like so:

.. code-block:: python

    cell = craton.cells.get(cell_id)
    cell_vars = cell.variables.get()

To update them:

.. code-block:: python

    updated_vars = {
        'var-a': 'new-var-a',
        'var-b': 'new-var-b',
        'updated-var': 'updated value',
    }
    cell.variables.update(**updated_vars)

To delete them:

.. code-block:: python

    cell.variables.delete('var-a', 'var-b', 'updated-var')

Updating a Cell
---------------

We can update a cell's attributes (but not its variables) like so:

.. code-block:: python

    craton.cells.update(
        cell_id,
        name='new name',
        note='Updated note.',
    )

Most attributes that you can specify on creation can also be specified for
updating the cell as well.

Deleting a Cell
---------------

We can delete with only its id:

.. code-block:: python

    craton.cells.delete(cell_id)
