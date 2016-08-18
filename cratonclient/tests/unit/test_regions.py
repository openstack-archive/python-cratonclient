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
    def test_host_create_unknown_error(self, m):
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
                          name='test')
