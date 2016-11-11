# Copyright (c) 2016 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Integration tests for the cratonclient.caching module."""
import tempfile

import dogpile.cache
from oslo_utils import uuidutils

from cratonclient import caching
from cratonclient.tests import base

PROJECT1 = uuidutils.generate_uuid()


class TestConfigure(base.TestCase):
    """Tests that ensure the configure function works properly."""

    def setUp(self):
        """Set up a temporary file for testing configure."""
        super(TestConfigure, self).setUp()
        self.tempfile = tempfile.NamedTemporaryFile()
        self.filename = self.tempfile.name
        self.addCleanup(self.tempfile.close)

    def test_returns_a_dogpile_cache_region(self):
        """Verify we return the dogpile.cache.region.CacheRegion instance."""
        region = caching.configure(caching.Cache.in_memory)

        self.assertIsInstance(region, dogpile.cache.region.CacheRegion)

    def test_returns_a_configured_in_memory_cache_region(self):
        """Verify we have correctly configured the CacheRegion."""
        region = caching.configure(caching.Cache.in_memory)

        self.assertEqual('cratonclient', region.name)
        self.assertTrue(region.is_configured)

    def test_returns_a_configured_on_disk_cache_region(self):
        """Verify we have correctly configured the CacheRegion."""
        region = caching.configure(caching.Cache.on_disk,
                                   filename=self.filename)

        self.assertEqual('cratonclient', region.name)
        self.assertTrue(region.is_configured)

    def test_returns_a_configured_using_memcached_region(self):
        """Verify we have correctly configured the CacheRegion."""
        region = caching.configure(caching.Cache.using_memcached,
                                   url='127.0.0.1:11211')

        self.assertEqual('cratonclient', region.name)
        self.assertTrue(region.is_configured)


class TestCreateSession(base.TestCase):
    """Tests that ensure the create_session integrates nicely."""

    def test_that_we_return_a_configured_session_with_caching(self):
        """Verify create_session does all that it says it will and more."""
        session = caching.create_session(
            username='demo',
            token='demo',
            project_id=PROJECT1,
            cache=caching.Cache.in_memory,
        )

        self.assertIsInstance(
            session._cache_region,
            dogpile.cache.region.CacheRegion,
        )

    def test_we_allow_configure_value_error_to_bubble_up(self):
        """Verify create_session allows the ValueError to bubble up."""
        self.assertRaises(
            ValueError,
            caching.create_session, cache='dogpile.cache.dbm'
        )
