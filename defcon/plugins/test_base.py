"""Tests for defcon.plugins.base."""
from django import test

from defcon.plugins import base


class PluginsTests(test.TestCase):
    """Test the plugins."""

    def test_plugin(self):
        """Test that we can build plugins."""
        class _FakePlugin(base.Plugin):
            """Fake class for testing."""

            def __init__(self, settings):
                """Fake __init__."""
                super(_FakePlugin, self).__init__(settings)

            def statuses(self):
                """Fake statuses."""
                return []

        # Can we instantiate it ?
        _FakePlugin({})
