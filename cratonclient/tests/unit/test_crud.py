# -*- coding: utf-8 -*-

# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
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
"""Unit tests for the cratonclient.crud module members."""

import mock

from cratonclient import crud
from cratonclient.tests import base


class TestCRUDClient(base.TestCase):
    """Test for the CRUDClient class."""

    def setUp(self):
        """Create necessary test resources prior to each test."""
        super(TestCRUDClient, self).setUp()
        self.session = mock.Mock()
        self.resource_spec = mock.Mock(spec=crud.Resource)
        self.client = self.create_client()

    def create_client(self, **kwargs):
        """Create and configure a basic CRUDClient."""
        client = crud.CRUDClient(self.session, 'http://example.com/v1/',
                                 **kwargs)
        client.base_path = '/test'
        client.key = 'test_key'
        client.resource_class = self.resource_spec
        return client

    def test_strips_trailing_forward_slash_from_url(self):
        """Verify the client strips the trailing / in a URL."""
        self.assertEqual('http://example.com/v1', self.client.url)

    def test_builds_url_correctly_with_no_path_args(self):
        """Verify the generated URL from CRUDClient#build_url without args."""
        self.assertEqual(
            'http://example.com/v1/test',
            self.client.build_url(),
        )

    def test_builds_url_correctly_with_key(self):
        """Verify the generated URL from CRUDClient#build_url with key."""
        self.assertEqual(
            'http://example.com/v1/test/1',
            self.client.build_url({'test_key_id': '1'}),
        )

    def test_builds_url_correctly_with_path_args(self):
        """Verify the generated URL from CRUDClient#build_url with args."""
        self.assertEqual(
            'http://example.com/v1/test/1',
            self.client.build_url({
                'test_key_id': '1',
                'extra_arg': 'foo',
            }),
        )

    def test_build_url_allows_base_path_override(self):
        """Verify we can override the client's base_path attribute."""
        self.assertEqual(
            'http://example.com/v1/override/1',
            self.client.build_url({
                'test_key_id': '1',
                'base_path': '/override',
            }),
        )

    def test_merge_request_arguments(self):
        """Verify we include extra request arguments."""
        client = self.create_client(extra_id=4321)
        request_args = {}

        client.merge_request_arguments(request_args, skip_merge=False)
        self.assertEqual({'extra_id': 4321}, request_args)

    def test_merge_request_arguments_skips_merging(self):
        """Verify we include extra request arguments."""
        client = self.create_client(extra_id=4321)
        request_args = {}

        client.merge_request_arguments(request_args, skip_merge=True)
        self.assertEqual({}, request_args)

    def test_create_generates_a_post_request(self):
        """Verify that using our create method will POST to our service."""
        response = self.session.post.return_value = mock.Mock()
        response.json.return_value = {'name': 'fake-name', 'id': 1}

        self.client.create(name='fake-name')

        self.session.post.assert_called_once_with(
            'http://example.com/v1/test',
            json={'name': 'fake-name'},
        )
        self.resource_spec.assert_called_once_with(
            self.client,
            {'name': 'fake-name', 'id': 1},
            loaded=True,
        )

    def test_delete_generates_a_delete_request(self):
        """Verify that using our delete method will send DELETE."""
        response = self.session.delete.return_value = mock.Mock()
        response.status_code = 204

        self.client.delete(test_key_id='1')

        self.session.delete.assert_called_once_with(
            'http://example.com/v1/test/1',
            json=None,
            params={}
        )
        self.assertFalse(self.resource_spec.called)

    def test_delete_generates_a_delete_request_positionally(self):
        """Verify passing the id positionally works as well."""
        response = self.session.delete.return_value = mock.Mock()
        response.status_code = 204

        self.client.delete(1)

        self.session.delete.assert_called_once_with(
            'http://example.com/v1/test/1',
            json=None,
            params={}
        )
        self.assertFalse(self.resource_spec.called)

    def test_get_generates_a_get_request(self):
        """Verify that using our get method will GET from our service."""
        response = self.session.get.return_value = mock.Mock()
        response.json.return_value = {'name': 'fake-name', 'id': 1}

        self.client.get(test_key_id=1)

        self.session.get.assert_called_once_with(
            'http://example.com/v1/test/1',
        )
        self.resource_spec.assert_called_once_with(
            self.client,
            {'name': 'fake-name', 'id': 1},
            loaded=True,
        )

    def test_get_generates_a_get_request_positionally(self):
        """Verify passing the id positionally works as well."""
        response = self.session.get.return_value = mock.Mock()
        response.json.return_value = {'name': 'fake-name', 'id': 1}

        self.client.get(1)

        self.session.get.assert_called_once_with(
            'http://example.com/v1/test/1',
        )
        self.resource_spec.assert_called_once_with(
            self.client,
            {'name': 'fake-name', 'id': 1},
            loaded=True,
        )

    def test_list_generates_a_get_request(self):
        """Verify that using our list method will GET from our service."""
        response = mock.Mock()
        items = [{'name': 'fake-name', 'id': 1}]
        self.session.paginate.return_value = iter([(response, items)])

        next(self.client.list(sort='asc'))

        self.session.paginate.assert_called_once_with(
            'http://example.com/v1/test',
            autopaginate=True,
            items_key='test_keys',
            params={'sort': 'asc'},
            nested=False,
        )
        self.resource_spec.assert_called_once_with(
            self.client,
            {'name': 'fake-name', 'id': 1},
            loaded=True,
        )

    def test_update_generates_a_put_request(self):
        """Verify that using our update method will PUT to our service."""
        response = self.session.put.return_value = mock.Mock()
        response.json.return_value = {'name': 'fake-name', 'id': 1}

        self.client.update(test_key_id='1', name='new-name')

        self.session.put.assert_called_once_with(
            'http://example.com/v1/test/1',
            json={'name': 'new-name'},
        )
        self.resource_spec.assert_called_once_with(
            self.client,
            {'name': 'fake-name', 'id': 1},
            loaded=True,
        )

    def test_update_generates_a_put_request_positionally(self):
        """Verify passing the id positionally works as well."""
        response = self.session.put.return_value = mock.Mock()
        response.json.return_value = {'name': 'fake-name', 'id': 1}

        self.client.update(1, name='new-name')

        self.session.put.assert_called_once_with(
            'http://example.com/v1/test/1',
            json={'name': 'new-name'},
        )
        self.resource_spec.assert_called_once_with(
            self.client,
            {'name': 'fake-name', 'id': 1},
            loaded=True,
        )


class TestResource(base.TestCase):
    """Tests for our crud.Resource object."""

    def setUp(self):
        """Create necessary fixture data for our Resource tests."""
        super(TestResource, self).setUp()
        self.manager = mock.Mock()
        self.info = {'name': 'fake-name', 'id': 1234}
        self.resource = crud.Resource(self.manager, self.info)

    def test_data_storage(self):
        """Verify we store our info privately."""
        self.assertEqual(self.info, self.resource._info)

    def test_manager(self):
        """Verify we store the manager passed in."""
        self.assertIs(self.manager, self.resource.manager)

    def test_human_id_is_false(self):
        """Test that None is returned when HUMAN_ID is False."""
        self.assertIsNone(self.resource.human_id)

    def test_human_id_is_true(self):
        """Verify we return our human-readable name."""
        self.resource.HUMAN_ID = True

        self.assertEqual('fake-name', self.resource.human_id)

    def test_info_is_converted_to_attributes(self):
        """Verify we add info data as attributes."""
        self.assertEqual('fake-name', getattr(self.resource, 'name'))
        self.assertEqual(1234, getattr(self.resource, 'id'))

    def test_retrieves_info_when_not_loaded(self):
        """Verify the resource tries to retrieve data from the service."""
        self.manager.get.return_value._info = {'non_existent': 'foo'}

        self.assertEqual('foo', self.resource.non_existent)
        self.manager.get.assert_called_once_with(1234)

    def test_raises_attributeerror_for_missing_attributes_when_loaded(self):
        """Verify we raise an AttributeError for missing attributes."""
        self.resource.set_loaded(True)

        self.assertRaises(
            AttributeError,
            getattr, self.resource, 'non_existent',
        )

    def test_equality(self):
        """Verify we check for equality correctly."""
        manager = mock.Mock()
        info = {'name': 'fake-name', 'id': 1234}
        new_resource = crud.Resource(manager, info)
        self.assertEqual(new_resource, self.resource)

    def test_to_dict_clones(self):
        """Prove that we return a new dictionary from to_dict."""
        self.assertIsNot(self.info, self.resource.to_dict())

    def test_to_dict_equality(self):
        """Prove that the new dictionary is equal."""
        self.assertEqual(self.info, self.resource.to_dict())

    def test_delete_calls_manager_delete(self):
        """Verify the manager's delete method is called."""
        self.resource.delete()

        self.manager.delete.assert_called_once_with(1234)

    def test_defaults_to_unloaded(self):
        """Verify by default a Resource is not loaded."""
        self.assertFalse(self.resource.is_loaded())

    def test_set_loaded_updates_loaded_status(self):
        """Verify set_loaded updates our loaded status."""
        self.resource.set_loaded(True)
        self.assertTrue(self.resource.is_loaded())
        self.resource.set_loaded(False)
        self.assertFalse(self.resource.is_loaded())

    def test_get_updates_with_new_info(self):
        """Verify we change the attribute values for new info."""
        self.manager.get.return_value._info = {'name': 'new-name'}

        self.resource.get()
        self.assertTrue(self.resource.is_loaded())
        self.assertEqual('new-name', self.resource.name)

    def test_get_updates_for_no_new_info(self):
        """Verify we don't add new details when there's nothing to add."""
        self.manager.get.return_value = None

        self.resource.get()
        self.assertTrue(self.resource.is_loaded())
        self.assertEqual('fake-name', self.resource.name)
