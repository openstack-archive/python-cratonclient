#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""Tests the host python client API in `cratonclient.v1.hosts` module."""
import json
import requests_mock

from cratonclient import exceptions as exc
from cratonclient.tests import base


class TestHosts(base.ShellTestCase):
    """Test our craton hosts shell commands."""

    def new_host(self, **kwargs):
        """Create a new Host test object."""
        kwargs.setdefault('id', 1)
        kwargs.setdefault('name', 'test')
        kwargs.setdefault('project_id', 1)
        kwargs.setdefault('region_id', 1)
        kwargs.setdefault('ip_address', '127.0.0.1')
        kwargs.setdefault('device_type', 'type')
        return kwargs

    def new_error(self, status, message):
        """Create a new error response object."""
        return {'status': status, 'message': message}

    @requests_mock.mock()
    def test_host_create_success(self, m):
        """Verify that all required args results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        host_reg = self.new_host()
        m.post('http://example.com/hosts',
               text=json.dumps(host_reg),
               status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        host = client.hosts.create(
            name='test',
            project_id='1',
            region_id='1',
            ip_address='127.0.0.1',
            device_type='type')
        self.assertEqual(host_reg, host._info)

    @requests_mock.mock()
    def test_host_create_unknown_error(self, m):
        """Verify what happens when an exception is raised."""
        from cratonclient import session
        from cratonclient.v1 import client

        host_reg = self.new_host()
        m.post('http://example.com/hosts',
               text=json.dumps(host_reg),
               status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError,
                          client.hosts.create,
                          name='test',
                          project_id='1',
                          region_id='1',
                          ip_address='127.0.0.1',
                          device_type='type')

    @requests_mock.mock()
    def test_host_get_success(self, m):
        """Verify that host get results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        host_reg = self.new_host()
        m.get('http://example.com/hosts/1',
              text=json.dumps(host_reg),
              status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        host = client.hosts.get(1)
        self.assertEqual(host_reg, host._info)

    @requests_mock.mock()
    def test_host_get_not_found(self, m):
        """Verify that host get results in not found exception."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(404, 'Not Found')
        m.get('http://example.com/hosts/1',
              text=json.dumps(error),
              status_code=404)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.NotFound, client.hosts.get, 1)

    @requests_mock.mock()
    def test_host_get_unknown_error(self, m):
        """Verify that host get results in unknown error."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.get('http://example.com/hosts/1',
              text=json.dumps(error),
              status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError, client.hosts.get, 1)

    @requests_mock.mock()
    def test_host_update_success(self, m):
        """Verify that update results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        host_reg = self.new_host()
        m.put('http://example.com/hosts/1',
              text=json.dumps(host_reg),
              status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        host = client.hosts.update(1, region_id=2)
        self.assertEqual(host_reg, host._info)

    @requests_mock.mock()
    def test_host_update_unknown_error(self, m):
        """Verify that host get results in unknown error."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.put('http://example.com/hosts/1',
              text=json.dumps(error),
              status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError, client.hosts.update, 1)

    @requests_mock.mock()
    def test_host_delete_success(self, m):
        """Verify that host delete results in success."""
        from cratonclient import session
        from cratonclient.v1 import client

        m.delete('http://example.com/hosts/1',
                 status_code=200)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        host = client.hosts.delete(1)
        self.assertEqual(None, host)

    @requests_mock.mock()
    def test_host_delete_unknown_error(self, m):
        """Verify that host delete results in unknown error."""
        from cratonclient import session
        from cratonclient.v1 import client

        error = self.new_error(500, 'Unknown Error')
        m.delete('http://example.com/hosts/1',
                 text=json.dumps(error),
                 status_code=500)
        session = session.Session(
            username='demo',
            token='password',
            project_id='1')
        client = client.Client(session, 'http://example.com')
        self.assertRaises(exc.InternalServerError, client.hosts.delete, 1)
