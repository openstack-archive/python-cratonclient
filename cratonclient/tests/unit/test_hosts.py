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
    def test_host_create_exception(self, m):
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
