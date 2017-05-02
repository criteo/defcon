"""Tests for defcon.status."""
import io
import unittest.mock

from django import test
from django.core import management
from django.utils import timezone

from defcon import plugins
from defcon.status import models
from defcon.status import views


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


class FakePlugin(plugins.static.StaticPlugin):
    @property
    def short_name(self):
        return 'fake'

    @property
    def name(self):
        return 'Fake plugin'


DEFCON_PLUGINS=['defcon.status.tests.FakePlugin']


@test.utils.override_settings(DEFCON_PLUGINS=DEFCON_PLUGINS)
class TestLoadPluginsCommand(test.TestCase):
    """
    Test the run plugins command
    """
    def test_add_plugin(self):
        out = io.StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

        plugin = FakePlugin()
        self.assertIn("Created %s" % plugin.name, out.getvalue())

        plugin_model = models.Plugin.objects.get(id=plugin.short_name)
        self.assertEqual(plugin_model.id, plugin.short_name)
        self.assertEqual(plugin_model.name, plugin.name)
        self.assertEqual(plugin_model.description, plugin.description)
        self.assertEqual(plugin_model.link, plugin.link)
        self.assertEqual(plugin_model.py_module, DEFCON_PLUGINS[0])

    def test_update_plugin(self):
        out = io.StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

        with unittest.mock.patch.object(FakePlugin, "name", "Updated Fake"):
            management.call_command('loadplugins', stdout=out)

            plugin = FakePlugin()
            self.assertIn("Updated %s" % plugin.name, out.getvalue())

            plugin_model = models.Plugin.objects.get(id=plugin.short_name)
            self.assertEqual(plugin_model.name, plugin.name)

    def test_remove_plugin(self):
        out = io.StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

        with self.settings(DEFCON_PLUGINS=[]):
            management.call_command('loadplugins', stdout=out)
            self.assertIn('Removed', out.getvalue())
            self.assertEqual(0, len(models.Plugin.objects.all()))
