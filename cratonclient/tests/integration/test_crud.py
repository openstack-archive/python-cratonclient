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
"""Integration tests for the cratonclient.crud module members."""

import mock

from cratonclient import crud
from cratonclient import exceptions as exc
from cratonclient import session
from cratonclient.tests import base


class TestCrudIntegration(base.TestCase):
    """Integration tests for CRUDClient and Resource classes."""

    def setUp(self):
        """Create necessary test resources prior to each test."""
        super(TestCrudIntegration, self).setUp()
        self.session = mock.Mock()
        self.craton_session = session.Session(session=self.session)
        self.client = self.create_client()

    def create_client(self, **kwargs):
        """Create and configure a basic CRUDClient."""
        client = crud.CRUDClient(
            session=self.craton_session,
            url='http://example.com/v1/',
            **kwargs
        )
        client.base_path = '/test'
        client.key = 'test_key'
        client.resource_class = crud.Resource
        return client

    def create_response(self,
                        status_code=200,
                        headers={},
                        json_return_value=None):
        """Create and configure a mock Response object."""
        response = mock.Mock(
            status_code=status_code,
            headers=headers,
        )
        response.json.return_value = json_return_value
        return response

    def test_create(self):
        """Verify our create makes it to the underlying session correctly."""
        self.session.request.return_value = self.create_response(
            status_code=201,
            json_return_value={'name': 'Test', 'id': 1234},
        )

        resource = self.client.create(
            nested_attr={'fake': 'data'},
            shallow_attr='first-level',
        )

        self.session.request.assert_called_once_with(
            method='POST',
            url='http://example.com/v1/test',
            json={'nested_attr': {'fake': 'data'},
                  'shallow_attr': 'first-level'},
            endpoint_filter={'service_type': 'fleet_management'},
        )
        self.assertIsInstance(resource, crud.Resource)
        self.assertEqual('Test', resource.name)
        self.assertEqual(1234, resource.id)

    def test_successful_delete(self):
        """Verify our delete returns True for a successful delete."""
        self.session.request.return_value = self.create_response(
            status_code=204,
        )

        self.assertTrue(self.client.delete(1))

    def test_not_successful_delete(self):
        """Verify our delete returns False for a failed delete."""
        self.session.request.return_value = self.create_response(
            status_code=404,
        )

        self.assertRaises(exc.NotFound, self.client.delete, 1)

    def test_delete_request(self):
        """Verify our delete request."""
        self.session.request.return_value = self.create_response(
            status_code=204,
        )

        self.client.delete(1)

        self.session.request.assert_called_once_with(
            method='DELETE',
            url='http://example.com/v1/test/1',
            json=None,
            params={},
            endpoint_filter={'service_type': 'fleet_management'},
        )

    def test_get(self):
        """Verify the request to retrieve an item."""
        self.session.request.return_value = self.create_response(
            status_code=200,
            json_return_value={'name': 'Test', 'id': 1234},
        )

        resource = self.client.get(1)

        self.session.request.assert_called_once_with(
            method='GET',
            url='http://example.com/v1/test/1',
            endpoint_filter={'service_type': 'fleet_management'},
        )
        self.assertIsInstance(resource, crud.Resource)
        self.assertEqual('Test', resource.name)
        self.assertEqual(1234, resource.id)

    def test_list(self):
        """Verify the request to list a resource."""
        self.session.request.return_value = self.create_response(
            status_code=200,
            json_return_value={
                'test_keys': [{'name': 'Test', 'id': 1234}],
                'links': [],
            },
        )

        resources = list(self.client.list(filter_by='some-attribute'))

        self.session.request.assert_called_once_with(
            method='GET',
            url='http://example.com/v1/test',
            params={'filter_by': 'some-attribute'},
            endpoint_filter={'service_type': 'fleet_management'},
        )

        for resource in resources:
            self.assertIsInstance(resource, crud.Resource)
            self.assertEqual('Test', resource.name)
            self.assertEqual(1234, resource.id)

    def test_update(self):
        """Verify the request to update a resource."""
        self.session.request.return_value = self.create_response(
            status_code=200,
            json_return_value={'name': 'Test', 'id': 1234},
        )

        resource = self.client.update(1234, name='New Test')

        self.session.request.assert_called_once_with(
            method='PUT',
            url='http://example.com/v1/test/1234',
            json={'name': 'New Test'},
            endpoint_filter={'service_type': 'fleet_management'},
        )
        self.assertIsInstance(resource, crud.Resource)
        self.assertEqual('Test', resource.name)
        self.assertEqual(1234, resource.id)
