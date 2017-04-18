"""Tests for defcon.status."""
from django import test
from django.utils import timezone

from defcon.status import models
from defcon.status import views
from defcon.plugins import base


class ModelTest(test.TestCase):
    """Test the models."""

    def test_plugin_instance(self):
        """See if we can create plugin instances."""
        p = models.Plugin.objects.create()
        pi = models.PluginInstance.objects.create(plugin=p)
        self.assertEqual(pi.component, None)

    def test_status(self):
        """See if we can use Status."""
        s = models.Status.objects.create(defcon=5)
        self.assertTrue(s.active)

        s.time_end = timezone.now().replace(year=1980)
        self.assertFalse(s.active)

        s.time_end = None
        s.time_start = timezone.now().replace(year=2030)
        self.assertFalse(s.active)


class ViewTest(test.TestCase):
    """Test the views."""

    def test_component_view_set(self):
        """See if they do stuff."""
        views.ComponentViewSet()


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
