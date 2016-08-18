"""Tests for `cratonclient.shell.v1.regions_shell` module."""
import mock
import re

from testtools import matchers

from cratonclient.tests import base


class TestRegionsShell(base.ShellTestCase):
    """Test craton regions shell commands."""

    re_options = re.DOTALL | re.MULTILINE

    def test_region_create_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-create',
            '.*?^craton region-create: error:.*$'
        ]
        stdout, stderr = self.shell('region-create')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.create')
    def test_region_create_success(self, mock_create):
        """Verify that all required create args results in success."""
        self.shell('region-create -n region')
        self.assertTrue(mock_create.called)

    def test_region_show_missing_required_args(self):
        """Verify that missing required args results in error message."""
        expected_responses = [
            '.*?^usage: craton region-show',
            '.*?^craton region-show: error:.*$',
        ]
        stdout, stderr = self.shell('region-show')
        for r in expected_responses:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(r, self.re_options))

    @mock.patch('cratonclient.v1.regions.RegionManager.get')
    def test_region_show_success(self, mock_get):
        """Verify that all required update args results in success."""
        self.shell('region-show 1')
        self.assertTrue(mock_get.called)