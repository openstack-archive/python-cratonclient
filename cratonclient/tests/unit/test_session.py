# -*- coding: utf-8 -*-

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
"""Session specific unit tests."""
from keystoneauth1 import session as ksa_session
import mock

from cratonclient import auth
from cratonclient import session
from cratonclient.tests import base


TEST_USERNAME_0 = 'test'
TEST_PROJECT_0 = 1
TEST_TOKEN_0 = 'fake-token'


class TestCratonAuth(base.TestCase):
    """Craton authentication keystoneauth plugin tests."""

    def test_stores_authentication_details(self):
        """Verify that our plugin stores auth details."""
        plugin = auth.CratonAuth(username=TEST_USERNAME_0,
                                 project_id=TEST_PROJECT_0,
                                 token=TEST_TOKEN_0)
        self.assertEqual(TEST_USERNAME_0, plugin.username)
        self.assertEqual(TEST_PROJECT_0, plugin.project_id)
        self.assertEqual(TEST_TOKEN_0, plugin.token)

    def test_generates_appropriate_headers(self):
        """Verify we generate the X-Auth-* headers."""
        fake_session = object()
        plugin = auth.CratonAuth(username=TEST_USERNAME_0,
                                 project_id=TEST_PROJECT_0,
                                 token=TEST_TOKEN_0)
        self.assertDictEqual(
            {
                'X-Auth-Token': TEST_TOKEN_0,
                'X-Auth-User': TEST_USERNAME_0,
                'X-Auth-Project': '{}'.format(TEST_PROJECT_0),
            },
            plugin.get_headers(fake_session)
        )

    def test_stores_token(self):
        """Verify get_token returns our token."""
        fake_session = object()
        plugin = auth.CratonAuth(username=TEST_USERNAME_0,
                                 project_id=TEST_PROJECT_0,
                                 token=TEST_TOKEN_0)

        self.assertEqual(TEST_TOKEN_0, plugin.get_token(fake_session))


class TestSession(base.TestCase):
    """Unit tests for cratonclient's Session abstraction."""

    @staticmethod
    def create_response(items, next_link):
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {
            'items': items,
            'links': [{
                'rel': 'next',
                'href': next_link,
            }],
        }
        return response

    def test_creates_keystoneauth_session(self):
        """Verify we default to keystoneauth sessions and semantics."""
        craton_session = session.Session(username=TEST_USERNAME_0,
                                         project_id=TEST_PROJECT_0,
                                         token=TEST_TOKEN_0)

        self.assertIsInstance(craton_session._session, ksa_session.Session)

    def test_will_use_the_existing_session(self):
        """Verify we don't overwrite an existing session object."""
        ksa_session_obj = ksa_session.Session()
        craton_session = session.Session(session=ksa_session_obj)

        self.assertIs(ksa_session_obj, craton_session._session)

    def test_paginate_stops_with_first_empty_list(self):
        """Verify the behaviour of Session#paginate."""
        response = self.create_response(
            [], 'http://example.com/v1/items?limit=30&marker=foo'
        )
        mock_session = mock.Mock()
        mock_session.request.return_value = response

        craton_session = session.Session(session=mock_session)
        paginated_items = list(craton_session.paginate(
            url='http://example.com/v1/items',
            items_key='items',
            autopaginate=True,
        ))

        self.assertListEqual([(response, [])], paginated_items)
        mock_session.request.assert_called_once_with(
            method='GET',
            url='http://example.com/v1/items',
            endpoint_filter={'service_type': 'fleet_management'},
        )

    def test_paginate_follows_until_an_empty_list(self):
        """Verify that Session#paginate follows links."""
        responses = [
            self.create_response(
                [{'id': _id}],
                'http://example.com/v1/items?limit=30&marker={}'.format(_id),
            ) for _id in ['foo', 'bar', 'bogus']
        ]
        responses.append(self.create_response([], ''))
        mock_session = mock.Mock()
        mock_session.request.side_effect = responses

        craton_session = session.Session(session=mock_session)
        paginated_items = list(craton_session.paginate(
            url='http://example.com/v1/items',
            items_key='items',
            autopaginate=True,
        ))

        self.assertEqual(4, len(paginated_items))

        self.assertListEqual(
            mock_session.request.call_args_list,
            [
                mock.call(
                    method='GET',
                    url='http://example.com/v1/items',
                    endpoint_filter={'service_type': 'fleet_management'},
                ),
                mock.call(
                    method='GET',
                    url='http://example.com/v1/items?limit=30&marker=foo',
                    endpoint_filter={'service_type': 'fleet_management'},
                ),
                mock.call(
                    method='GET',
                    url='http://example.com/v1/items?limit=30&marker=bar',
                    endpoint_filter={'service_type': 'fleet_management'},
                ),
                mock.call(
                    method='GET',
                    url='http://example.com/v1/items?limit=30&marker=bogus',
                    endpoint_filter={'service_type': 'fleet_management'},
                ),
            ],
        )
