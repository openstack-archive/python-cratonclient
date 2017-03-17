.. _usage-auth:

==========================
 Authenticating to Craton
==========================

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
