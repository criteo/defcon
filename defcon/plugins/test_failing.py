"""Tests for failing plugin."""
from django import test

from defcon.plugins import base
from defcon.plugins import failing


class FailingPluginTest(test.TestCase):
    """Test the failing plugin."""

    def test_simple(self):
        """Test __init__."""
        p = failing.failingPlugin()
        self.assertEquals(p.short_name, 'failing')

        s = base.Status('title')
        p = failing.FailingPlugin({'statuses': [s]})
        with self.assertRaises(Exception):
            p.statuses()
