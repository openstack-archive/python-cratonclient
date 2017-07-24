=======================
 Craton CLI User Guide
=======================

After installing ``python-cratonclient`` and ``craton`` binary should be added
to our PATH. To use the craton command-line client, we need the following
information:

- URL to speak to Craton with

- Username to use to authenticate to Craton

- Password to use to authenticate to Craton

- Project ID to use to communicate with Craton

These items need to be provided to the craton command-line client. We can pass
these as command-line arguments:

.. code::

    $ craton --craton-url <craton-url> \
             --os-username <username> \
             --os-password <password> \
             --os-project-id <project-id>

These parameters may also be provided via environment variables. We can create
a file, similar to OpenStack's ``openrc`` file that contains:

.. code-block:: bash

    # ~/cratonrc
    export CRATON_URL="<craton-url>"
    export OS_USERNAME="<username>"
    export OS_PASSWORD="<password>"
    export OS_PROJECT_ID="<project-id>"

And then ``source`` it into our environment:

.. code::

    $ source ~/cratonrc
    # or
    $ . ~/cratonrc

And finally we can use ``craton`` without those parameters.


Top-Level Options
=================

Craton's command-line client has several top-level options. These are required
to be specified prior to any sub-command. All of craton's top-level
command-line options are documented here:

..
    OPTION TEMPLATE
    --------------------------8<---------------------------------------
    .. option:: --<opt-name>[=<descriptive-parameter-name>]

        <Active description of the purpose.>

        Example usage:

        .. code::

            $ craton --<opt-name>[=<example value>] [positional args]
    -------------------------->8---------------------------------------


.. program:: craton

.. option:: --version

    Show the installed version of python-cratonclient.

    Example usage:

    .. code::

        $ craton --version

.. option:: --format={default,json}

    Specify the format of the output to the terminal. The default value is a
    pretty-printed table of information. Alternatively, users may request
    pretty-printed JSON.

    Example usage:

    .. code::

        $ craton --format=json host-list
        $ craton --format=json region-show 1

.. option:: --craton-url=URL

    Specify the URL where Craton is reachable.

    Example usage:

    .. code::

        $ craton --craton-url=:https://craton.cloud.corp host-list

.. option:: --craton-version=VERSION

    Control which version of Craton's API the client should use to
    communicate. At the moment, Craton only supports ``1`` for v1.

    Example usage:

    .. code::

        $ craton --craton-version=1 region-list

.. option:: --os-project-id=OS_PROJECT_ID

    Provide the Project ID to use when authenticating to Craton.

    Example usage:

    .. code::

        $ craton --os-project-id=b9f10eca66ac4c279c139d01e65f96b4 cell-list

.. option:: --os-username=OS_USERNAME

    Provide the Username to use when authenticating to Craton.

    Example usage:

    .. code::

        $ craton --os-username=demo project-list

.. option:: --os-password=OS_PASWORD

    Provide the Pasword to use when authenticating to Craton.

    Example usage:

    .. code::

        $ craton --os-password=demo devices-list


Subcommands
===========

The craton command-line client has several subcommands. These include (but are
not limited to):

- ``help``

- ``project-create``

- ``project-delete``

- ``project-list``

- ``project-show``

- ``cloud-create``

- ``cloud-delete``

- ``cloud-list``

- ``cloud-show``

- ``region-create``

- ``region-delete``

- ``region-list``

- ``region-show``

- ``cell-create``

- ``cell-delete``

- ``cell-list``

- ``cell-show``

- ``host-create``

- ``host-delete``

- ``host-list``

- ``host-show``

- ``device-list``.

The command-line options available for each command can be found via
``craton help <subcommand-name>``, e.g.,

.. code::

    $ craton help cell-create
    $ craton help host-list
