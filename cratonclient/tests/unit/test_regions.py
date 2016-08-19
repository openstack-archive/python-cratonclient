# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests the region python client API in `cratonclient.v1.regions` module."""
import json
import requests_mock

from cratonclient import exceptions as exc
from cratonclient.tests import base


class TestRegions(base.TestCase):
    """Test craton regions python client."""

    def new_region(self, **kwargs):
        """Create a new Region test object."""
        kwargs.setdefault('id', 1)
        kwargs.setdefault('project_id', 1)
        kwargs.setdefault('name', 'region')
        return kwargs

    def new_error(self, status, message):
        """Create a mew error response object."""
        return {'status': status, 'message': message}

    @requests_mock.mock()
    def test_region_create_success(self, m):
        """Verify all required args results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        reg = self.new_region()
        m.post('http://example.com/regions',
               text=json.dumps(reg),
               status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        region = client.regions.create(name='region')
        self.assertEqual(reg, region._info)

    @requests_mock.mock()
    def test_region_create_unknown_error(self, m):
        """Verify what happens when an exception is raised."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.post('http://example.com/regions',
               text=json.dumps(error),
               status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError,
                          client.regions.create,
                          name='region')

    @requests_mock.mock()
    def test_region_get_success(self, m):
        """Verify that region get results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        reg = self.new_region()
        m.get('http://example.com/regions/1',
              text=json.dumps(reg),
              status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        region = client.regions.get(1)
        self.assertEqual(reg, region._info)

    @requests_mock.mock()
    def test_region_get_not_found(self, m):
        """Verify that region get results in not found exception."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(404, 'Not Found')
        m.get('http://example.com/regions/1',
              text=json.dumps(error),
              status_code=404)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.NotFound, client.regions.get, 1)

    @requests_mock.mock()
    def test_region_get_unknown_error(self, m):
        """Verify that region get results in unknown error."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.get('http://example.com/regions/1',
              text=json.dumps(error),
              status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError, client.regions.get, 1)

    @requests_mock.mock()
    def test_region_update_success(self, m):
        """Verify that update results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        reg = self.new_region()
        m.put('http://example.com/regions/1',
              text=json.dumps(reg),
              status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        region = client.regions.update(1, name='new_region')
        self.assertEqual(reg, region._info)

    @requests_mock.mock()
    def test_region_update_unknown_error(self, m):
        """Verify that region update results in unknown error."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.put('http://example.com/regions/1',
              text=json.dumps(error),
              status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError, client.regions.update, 1)

    @requests_mock.mock()
    def test_region_delete_success(self, m):
        """Verify that region delete results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        m.delete('http://example.com/regions/1', status_code=200)
        session = session.Session(username='demo',
                                  token='password',
                                  project_id=1)
        client = client.Client(session, 'http://example.com')
        region = client.regions.delete(1)
        self.assertEquals(None, region)

    @requests_mock.mock()
    def test_region_delete_unknown_error(self, m):
        """Verify that region delete results in unknown error."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.delete('http://example.com/regions/1',
                 text=json.dumps(error),
                 status_code=500)
        session = session.Session(username='demo',
                                  token='password',
                                  project_id=1)
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError, client.regions.delete, 1)
