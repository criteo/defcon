"""Tests for static plugin."""
from django import test

from defcon.plugins import base
from defcon.plugins import static


class StaticPluginTest(test.TestCase):
    """Test the static plugin."""

    def test_simple(self):
        """Test __init__."""
        p = static.StaticPlugin()
        self.assertEquals(p.short_name, 'static')

        s = base.Status('test', 2, 'test')
        p = static.StaticPlugin({'statuses': [s]})
        self.assertEquals(p.statuses(), {s['id']: s})
