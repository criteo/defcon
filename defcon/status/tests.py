"""Tests for defcon.status."""
from django import test

from defcon.status import models
from defcon.status import views


class ModelTestCase(test.TestCase):
    """Test the models."""

    def test_plugin_instance(self):
        """See if we can create plugin instances."""
        p = models.Plugin.objects.create()
        pi = models.PluginInstance.objects.create(plugin=p)
        self.assertEqual(pi.component, None)


class ViewTestcase(test.TestCase):
    """Test the views."""

    def test_component_view_set(self):
        """See if they do stuff."""
        views.ComponentViewSet()
