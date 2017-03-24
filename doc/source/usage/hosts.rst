=====================
 Using the Hosts API
=====================

Here we will assume that we already have a
:class:`~cratonclient.client.Client` instance configured with the appropriate
authentication method (as demonstrated in :ref:`usage-auth`).

Listing Hosts
-------------

The Hosts API implements pagination. This means that by default, it does not
return all hosts known to Craton. To ignore page limits and offsets, we can
allow cratonclient to do handle pagination for us:

.. code-block:: python

   for host in craton.hosts.list():
       print_host_info(host)

By default :meth:`~cratonclient.v1.hosts.HostManager.list` will handle
pagination for you. If, instead, you want to handle it yourself you will want
to do something akin to:

.. code-block:: python

    first_page_of_hosts = list(craton.hosts.list(autopaginate=False))
    marker_id = first_page_of_hosts[-1].id
    second_page_of_hosts = list(craton.hosts.list(
        autopaginate=False,
        marker=marker_id,
    ))
    marker_id = second_page_of_hosts[-1].id
    third_page_of_hosts = list(craton.hosts.list(
        autopaginate=False,
        marker=marker_id,
    ))
    # etc.

A more realistic example, however, might look like this:

.. code-block:: python

    hosts_list = None
    marker = None
    while hosts_list and hosts_list is not None:
        hosts_list = list(craton.hosts.list(
            marker=marker,
            autopaginate=False,
        ))
        # do something with hosts_list
        if hosts_list:
            marker = hosts_list[-1].id

This will have the effect of stopping the while loop when you eventually
receive an empty list from ``craton.hosts.list(...)``.

Creating Hosts
--------------

Hosts live inside either a Region or Cell in Craton. To create a host, one
needs:

- A unique name

- A unique IP address

- A "device type" (this is freeform), e.g., "server", "container", "nova-vm",
  etc.

- A cloud ID

- A region ID

.. code-block:: python

    host = craton.hosts.create(
        name='my-host-0',
        ip_address='127.0.1.0',
        device_type='server',
        cloud_id=cloud_id,
        region_id=region_id,
        note='This is my host, there are many like it, but this is mine.',
        variables={
            'some-var': 'some-var-value',
        },
    )

Retrieving a Specific Host
--------------------------

Hosts can be retrieved by id.

.. code-block:: python

    host = craton.hosts.get(1)

Using a Host's Variables
------------------------

Once we have a host we can introspect its variables like so:

.. code-block:: python

    host = craton.hosts.get(host_id)
    host_vars = host.variables.get()

To update them:

.. code-block:: python

    updated_vars = {
        'var-a': 'new-var-a',
        'var-b': 'new-var-b',
        'updated-var': 'updated value',
    }
    host.variables.update(**updated_vars)

To delete them:

.. code-block:: python

    host.variables.delete('var-a', 'var-b', 'updated-var')

Updating a Host
---------------

We can update a host's attributes (but not its variables) like so:

.. code-block:: python

    craton.hosts.update(
        host_id,
        name='new name',
        note='Updated note.',
    )

Most attributes that you can specify on creation can also be specified for
updating the host as well.

Deleting a Host
---------------

We can delete with only its id:

.. code-block:: python

    craton.hosts.delete(host_id)
