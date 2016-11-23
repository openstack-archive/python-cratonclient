=======================
 Python API User Guide
=======================

Once you have installed ``python-cratonclient``, there are a few things you
need to get started using the Python API:

#. You need to know how to authenticate to the Craton API you wish to talk to

   Some Craton API services will be deployed using Craton's in-built
   authentication system while others may use Keystone.

#. You need your credentials

#. You need the location of your Craton API service

Let's cover authentication first:


Authenticating to Craton
========================

There are two ways to authenticate to Craton:

#. Using Craton's in-built authentication system (the default)

#. Using Keystone

Craton Authentication
---------------------

In the Craton Authentication case, you need the URL for the Craton API
service, your username, project ID, and token. To set up cratonclient for this
authentication, you need only do the following:

.. code-block:: python

    from cratonclient import auth
    from cratonclient.v1 import client

    craton_session = auth.craton_auth(
        username=USERNAME,
        token=TOKEN,
        project_id=PROJECT_ID,
    )

    craton = client.Client(
        session=craton_session,
        url=URL,
    )

Keystone Authentication
-----------------------

When authenticating to Craton using Keystone, you need to know:

- the URL to use to authenticate to Keystone which we will refer to as
  ``AUTH_URL``

- the username

- the password

- the project ID or name

- the user domain ID or name

- and the project domain ID or name

Then, we need to do the following:

.. code-block:: python

    from keystoneauth1.identity.v3 import password as password_auth
    from keystoneauth1 import session as ksa_session

    from cratonclient import auth
    from cratonclient.v1 import client

    craton_session = auth.keystone_auth(
        auth_url=AUTH_URL,
        password=PASSWORD,
        username=USERNAME,
        user_domain_name=USER_DOMAIN_NAME,
        project_name=PROJECT_NAME,
        project_domain_name=PROJECT_DOMAIN_NAME,
    )
    craton = client.Client(
        session=craton_session,
        url=URL,
    )


Communicating with Craton
=========================

Now that you've configured your authentication method, you can interact with
your ``craton`` object like so:

.. code-block:: python

    for region in craton.regions.list():
        print('Region {} contains:'.format(region.name))
        for host in craton.hosts.list(region_id=region.id):
            print('    {}'.format(host.name))


The Craton API has the following resources:

- Cells

- Hosts

- Network Devices

- Network Interfaces

- Networks

- Projects

- Regions

- Users

Of these:

- Cells

- Hosts

- Regions

Are implemented.
