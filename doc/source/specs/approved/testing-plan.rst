..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
 Testing Plan for cratonclient
===============================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/python-cratonclient/+spec/testing-plan

The python-cratonclient presently has a couple hundred tests that ensure that
it does what we expect. At the moment, however, most of those tests use mocks
to force certain behaviours. While these are valuable tests, we need more real
world tests to ensure that the client *does* reflect the reality of the API.


Problem description
===================

Using Mocks inside tests can be a very valuable tool for writing fast tests
and reproducing issues that are otherwise difficult to do. Mocks, however, can
make tests incredibly fragile. To have a healthy test suite, we need tests
that avoid mocks altogether.


Proposed change
===============

The existing test suite is a good base to build a better test suite upon.
Going forward, we will *still* rely on Mock for *some* tests but we will
instead start to rely on other test methodologies for this client.

First we will implement a new type of integration testing. This will leverage
a library called `Betamax`_. This will allow us to have tests that use real
data and real responses from a Craton server without needing to set a server
up every single time. Betamax will record the requests and responses and allow
our tests to use the saved interactions (request, response pairs) instead of
requiring an active server to be configured.

Next we'll move our existing integration tests that heavily mock out the
layers below into the unit test directories unless they actually test some
level of integration (i.e., more than one level).

Finally we'll add the ability to run tests against a live server that will be
configured and managed by docker-py in a way similar to the Craton API
functional tests. These will be part of a separate tox test environment,
similar to the API tests.

Alternatives
------------

Much of the client relies on responses from the API. We could simply require
functional tests for every layer of the client library that interacts with the
API which would leave only utility functions for unit testing. This would
reduce the need for different tests at different levels. This would also
increase the run time of the default test suite by requiring docker containers
be launched for each one.


Security impact
---------------

If any impact, this may improve the posture by increasing the testing of the
user's surface area.

Other end user impact
---------------------

None

Performance Impact
------------------

None

Developer impact
----------------

This should be accompanied by developer documentation with information
determining what kind of test to write when and what tests belong in what
categories.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
- icordasc

Other contributors:
- None

Work Items
----------

- Add base framework for testing with Betamax.

- Add comprehensive integration tests for the Python API level.

- Move existing "integration" unit tests into appropriate unit test modules.

- Improve shell integration testing. Including parsing PrettyTable output and
  using the JSON formatter for better verification of reporting.

- Add functional tests against live Craton servers.


Dependencies
============

- None


Testing
=======

See above. =)


Documentation Impact
====================

This will require developer reference updates as noted above.


References
==========

N/A


.. links
.. _Betamax:
    https://pypi.org/project/betamax
