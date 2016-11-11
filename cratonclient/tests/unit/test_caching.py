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
"""Unit tests for the cratonclient.caching module."""
import mock

from oslo_utils import uuidutils

from cratonclient import caching
from cratonclient.tests import base

PROJECT1 = uuidutils.generate_uuid()


class TestCacheEnum(base.TestCase):
    """Tests for the Cache enum object."""

    def test_value_of_in_memory_enum(self):
        """Verify the value of the in_memory enum."""
        self.assertEqual('dogpile.cache.memory', caching.Cache.in_memory.value)

    def test_value_of_on_disk_enum(self):
        """Verify the value of the on_disk enum."""
        self.assertEqual('dogpile.cache.dbm', caching.Cache.on_disk.value)

    def test_value_of_using_memcached_enum(self):
        """Verify the value of the using_memcached enum."""
        self.assertEqual('dogpile.cache.memcached',
                         caching.Cache.using_memcached.value)


class TestConfigure(base.TestCase):
    """Tests for the configure function."""

    def setUp(self):
        """Create the necessary test resources for the configure tests."""
        super(TestConfigure, self).setUp()
        self.make_region_patch = mock.patch('dogpile.cache.make_region')
        self.make_region = self.make_region_patch.start()
        self.region = self.make_region.return_value = mock.Mock()
        self.addCleanup(self.make_region_patch.stop)

    def test_asserts_backends_are_enums(self):
        """Verify a cache backend must be a member of our Cache enum."""
        self.assertRaises(ValueError, caching.configure, 'dogpile.cache.dbm')

    def test_make_region_is_called_with_a_name(self):
        """Verify we provide a name to dogpile.cache.make_region."""
        caching.configure(caching.Cache.in_memory)

        self.make_region.assert_called_once_with(name='cratonclient')

    def test_does_not_provide_extra_config_for_in_memory_cache(self):
        """Do not pass along extra configuration arguments for in_memory."""
        caching.configure(caching.Cache.in_memory, expiration_time=3600)

        self.region.configure.assert_called_once_with('dogpile.cache.memory')

    def test_provides_extra_configuration_for_on_disk_cache(self):
        """Pass along extra configuration arguments for on_disk option."""
        caching.configure(caching.Cache.on_disk, expiration_time=3600,
                          filename='foo.dbm')

        self.region.configure.assert_called_once_with(
            'dogpile.cache.dbm', expiration_time=3600, arguments={
                'filename': 'foo.dbm',
            },
        )

    def test_provides_extra_configuration_for_using_memcached_cache(self):
        """Pass along extra configuration arguments for using_memcached."""
        caching.configure(caching.Cache.using_memcached, expiration_time=300,
                          url='10.10.1.9:11211')

        self.region.configure.assert_called_once_with(
            'dogpile.cache.memcached', expiration_time=300, arguments={
                'url': '10.10.1.9:11211',
            },
        )


class TestCreateSession(base.TestCase):
    """Tests for the create_session function."""

    def setUp(self):
        """Patch out the session object and configure function."""
        super(TestCreateSession, self).setUp()
        self.configure_patch = mock.patch('cratonclient.caching.configure')
        self.configure = self.configure_patch.start()
        self.addCleanup(self.configure_patch.stop)
        self.region = self.configure.return_value = mock.Mock()

        self.session_patch = mock.patch('cratonclient.session.Session')
        self.session_class = self.session_patch.start()
        self.addCleanup(self.session_patch.stop)
        self.session = self.session_class.return_value = mock.Mock()

    def test_creates_a_new_session_with_params(self):
        """Verify we create a craton session for the user."""
        caching.create_session(
            username='demo',
            token='demo',
            project_id=PROJECT1,
            cache=caching.Cache.in_memory,
        )

        self.session_class.assert_called_once_with(
            session=None,
            username='demo',
            token='demo',
            project_id=PROJECT1,
        )

    def test_configures_a_backend(self):
        """Verify we create a craton session for the user."""
        caching.create_session(
            username='demo',
            token='demo',
            project_id=PROJECT1,
            cache=caching.Cache.in_memory,
        )

        self.configure.assert_called_once_with(backend=caching.Cache.in_memory)

    def test_wraps_the_session_request_method(self):
        """Verify we wrap the session's request method with our region."""
        original_request_method = self.session.request
        caching.create_session(
            username='demo',
            token='demo',
            project_id=PROJECT1,
            cache=caching.Cache.in_memory,
        )

        self.region.cache_on_arguments.assert_called_once_with(
            original_request_method
        )
        self.assertIsNot(original_request_method, self.session.request)
        self.assertIs(self.region.cache_on_arguments.return_value,
                      self.session.request)

    def test_stores_cache_region_on_session(self):
        """Verify we store the configured region on the session."""
        caching.create_session(
            username='demo',
            token='demo',
            project_id=PROJECT1,
            cache=caching.Cache.in_memory,
        )

        self.assertIs(self.session._cache_region, self.region)
