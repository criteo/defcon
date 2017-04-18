"""Tests for static plugin."""
from django import test

from defcon.plugins import static


class StaticPluginTest(test.TestCase):
    """Test the static plugin."""

    def test_instantiate(self):
        """Test __init__."""
        p = static.StaticPlugin()
        self.assertEquals(p.short_name, 'static')
        p = static.StaticPlugin({'foo': 'bar'})
