========================
 Using the Projects API
========================

Here we will assume that we already have a
:class:`~cratonclient.client.Client` instance configured with the appropriate
authentication method (as demonstrated in :ref:`usage-auth`).

Listing Projects
----------------

The Projects API implements pagination. This means that by default, it does not
return all projects known to Craton. To ignore page limits and offsets, we can
allow cratonclient to do handle pagination for us:

.. code-block:: python

   for project in craton.projects.list():
       print_project_info(project)

By default :meth:`~cratonclient.v1.projects.ProjectManager.list` will handle
pagination for you. If, instead, you want to handle it yourself you will want
to do something akin to:

.. code-block:: python

    first_page_of_projects = list(craton.projects.list(autopaginate=False))
    marker_id = first_page_of_projects[-1].id
    second_page_of_projects = list(craton.projects.list(
        autopaginate=False,
        marker=marker_id,
    ))
    marker_id = second_page_of_projects[-1].id
    third_page_of_projects = list(craton.projects.list(
        autopaginate=False,
        marker=marker_id,
    ))
    # etc.

A more realistic example, however, might look like this:

.. code-block:: python

    projects_list = None
    marker = None
    while projects_list and projects_list is not None:
        projects_list = list(craton.projects.list(
            marker=marker,
            autopaginate=False,
        ))
        # do something with projects_list
        if projects_list:
            marker = projects_list[-1].id

This will have the effect of stopping the while loop when you eventually
receive an empty list from ``craton.projects.list(...)``.

Creating Projects
-----------------

Projects are top-level items in Craton. To create a project, one needs:

- A unique name

- Permission to create new projects


.. code-block:: python

    project = craton.projects.create(
        name='my-project-0',
        variables={
            'some-var': 'some-var-value',
        },
    )

Retrieving a Specific Project
-----------------------------

Projects can be retrieved by id.

.. code-block:: python

    project = craton.projects.get(1)

Using a Project's Variables
---------------------------

Once we have a project we can introspect its variables like so:

.. code-block:: python

    project = craton.projects.get(project_id)
    project_vars = project.variables.get()

To update them:

.. code-block:: python

    updated_vars = {
        'var-a': 'new-var-a',
        'var-b': 'new-var-b',
        'updated-var': 'updated value',
    }
    project.variables.update(**updated_vars)

To delete them:

.. code-block:: python

    project.variables.delete('var-a', 'var-b', 'updated-var')

Updating a Project
------------------

We can update a project's attributes (but not its variables) like so:

.. code-block:: python

    craton.projects.update(
        project_id,
        name='new name',
    )

Most attributes that you can specify on creation can also be specified for
updating the project as well.

Deleting a Project
------------------

We can delete with only its id:

.. code-block:: python

    craton.projects.delete(project_id)
