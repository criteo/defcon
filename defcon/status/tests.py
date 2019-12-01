"""Tests for defcon.status."""

# pylama:ignore=D102,D101

import contextlib
import copy
import sys

try:
    from unittest import mock
except ImportError:
    import mock

from django import test
from django.core import management
from django.utils import timezone

from defcon.plugins import base, static
from defcon.status import models
from defcon.status import views

if sys.version_info < (3, ):
    import StringIO as _StringIO
    StringIO = _StringIO.StringIO
else:
    import io
    StringIO = io.StringIO


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


class FakePlugin(static.StaticPlugin):
    @property
    def short_name(self):
        return 'fake'

    @property
    def name(self):
        return 'Fake plugin'


DEFCON_PLUGINS = ['defcon.status.tests.FakePlugin']


@test.utils.override_settings(DEFCON_PLUGINS=DEFCON_PLUGINS)
class TestLoadPluginsCommand(test.TestCase):
    """Test the run plugins command."""

    def test_add_plugin(self):
        out = StringIO()
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
        out = StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

        with mock.patch.object(FakePlugin, "name", "Updated Fake"):
            management.call_command('loadplugins', stdout=out)

            plugin = FakePlugin()
            self.assertIn("Updated %s" % plugin.name, out.getvalue())

            plugin_model = models.Plugin.objects.get(id=plugin.short_name)
            self.assertEqual(plugin_model.name, plugin.name)

    def test_remove_plugin(self):
        out = StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

        with self.settings(DEFCON_PLUGINS=[]):
            management.call_command('loadplugins', stdout=out)
            self.assertIn('Removed', out.getvalue())
            self.assertEqual(0, len(models.Plugin.objects.all()))


DEFCON_COMPONENTS = {
    'production': {
        'name': 'Production',
        'description': 'All the production perimeter.',
        'link': 'https://github.com/criteo/defcon/wiki/production',
        'contact': 'escalation@iksaif.net',
        'plugins': [],
    },
}


@test.utils.override_settings(DEFCON_PLUGINS=DEFCON_PLUGINS)
class TestLoadComponentsCommand(test.TestCase):
    def setUp(self):
        out = StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

    def test_add_component(self):
        out = StringIO()
        self.addCleanup(out.close)
        components = copy.deepcopy(DEFCON_COMPONENTS)
        component = components['production']

        with self.settings(DEFCON_COMPONENTS=components):
            management.call_command("loadcomponents", stdout=out)
            self.assertIn("Created %s" % component["name"], out.getvalue())

            component_model = models.Component.objects.get(id="production")
            self.assertEqual(component_model.name, component["name"])
            self.assertEqual(component_model.description,
                             component["description"])
            self.assertEqual(component_model.link, component["link"])
            self.assertEqual(component_model.contact, component["contact"])

    def test_add_component_with_plugins(self):
        out = StringIO()
        self.addCleanup(out.close)
        components = copy.deepcopy(DEFCON_COMPONENTS)
        plugin = {
            'plugin': 'fake',
            'name': 'test',
            'description': 'test plugin instance',
            'config': {'statuses': []},
        }
        components['production']['plugins'].append(plugin)

        with self.settings(DEFCON_COMPONENTS=components):
            management.call_command("loadcomponents", stdout=out)
            self.assertIn("Created Production:Fake", out.getvalue())

            component_model = models.Component.objects.get(id="production")
            plugin_model = component_model.plugins.first()
            self.assertEqual(plugin_model.name, plugin['name'])
            self.assertEqual(plugin_model.description, plugin['description'])
            self.assertEqual(plugin_model.plugin.id, plugin['plugin'])
            self.assertEqual(plugin_model.config, plugin['config'])

    def test_remove_component(self):
        out = StringIO()
        self.addCleanup(out.close)
        components = copy.deepcopy(DEFCON_COMPONENTS)

        with self.settings(DEFCON_COMPONENTS=components):
            management.call_command("loadcomponents", stdout=out)

        with self.settings(DEFCON_COMPONENTS={}):
            management.call_command("loadcomponents", stdout=out)
            self.assertIn('Removed production', out.getvalue())
            self.assertEqual(0, len(models.Component.objects.all()))

    def test_update_component(self):
        out = StringIO()
        self.addCleanup(out.close)
        components = copy.deepcopy(DEFCON_COMPONENTS)
        component = components['production']

        with self.settings(DEFCON_COMPONENTS=components):
            management.call_command("loadcomponents", stdout=out)

            component['description'] = 'Updated description'
            management.call_command("loadcomponents", stdout=out)
            self.assertIn("Updated Production", out.getvalue())

            component_model = models.Component.objects.get(id="production")
            self.assertEqual(component_model.description,
                             component['description'])

    def test_update_component_plugins(self):
        out = StringIO()
        self.addCleanup(out.close)
        components = copy.deepcopy(DEFCON_COMPONENTS)
        component = components['production']
        plugin = {
            'plugin': 'fake',
            'name': 'test',
            'description': 'test plugin instance',
            'config': {'statuses': []},
        }

        component['plugins'].append(plugin)

        with self.settings(DEFCON_COMPONENTS=components):
            management.call_command("loadcomponents", stdout=out)

            other_plugin = plugin.copy()
            other_plugin['name'] = "test2"
            plugin['description'] = 'updated description'
            component['plugins'].append(other_plugin)

            management.call_command("loadcomponents", stdout=out)
            component_model = models.Component.objects.get(id="production")

            test_plugin = test2_plugin = None

            for plugin_model in component_model.plugins.all():
                if plugin_model.name == "test":
                    test_plugin = plugin_model
                elif plugin_model.name == "test2":
                    test2_plugin = plugin_model
                else:
                    self.fail("Plugin %s must not exist" % plugin_model.name)

            if not (test_plugin and test2_plugin):
                self.fail("one plugin is missing")

            self.assertEqual(test_plugin.description, plugin['description'])


@test.utils.override_settings(DEFCON_PLUGINS=DEFCON_PLUGINS)
class TestRunPluginsCommand(test.TestCase):
    def setUp(self):
        out = StringIO()
        self.addCleanup(out.close)
        management.call_command('loadplugins', stdout=out)

    @test.utils.override_settings(DEFCON_COMPONENTS=DEFCON_COMPONENTS)
    def test_run_without_plugins(self):
        out = StringIO()
        self.addCleanup(out.close)

        management.call_command('runplugins', stdout=out)
        self.assertEqual("", out.getvalue())

    @contextlib.contextmanager
    def components_with_plugin(self, *statuses):
        components = copy.deepcopy(DEFCON_COMPONENTS)
        plugin = {
            'plugin': 'fake',
            'name': 'test',
            'description': 'test plugin instance',
            'config': {'statuses': list(statuses)},
        }
        components['production']['plugins'].append(plugin)

        out = StringIO()
        self.addCleanup(out.close)
        with self.settings(DEFCON_COMPONENTS=components):
            management.call_command('loadcomponents', stdout=out)
            yield components

    def test_run_add_status(self):
        out = StringIO()
        self.addCleanup(out.close)
        status = base.Status('Test status', 5, 'http://foo/#5')

        with self.components_with_plugin(status):
            management.call_command('runplugins', stdout=out)
            self.assertIn("Running test Production:Fake plugin", out.getvalue())
            self.assertIn("Created Fake plugin:Test status", out.getvalue())

            status_model = models.Status.objects.all()[0]

            self.assertEqual(status_model.title, status['title'])
            self.assertEqual(status_model.link, status['link'])
            self.assertEqual(status_model.description, status['description'])
            self.assertEqual(status_model.defcon, status['defcon'])
            self.assertFalse(status_model.override)

    def test_run_update_status(self):
        out = StringIO()
        self.addCleanup(out.close)
        status = base.Status('Test status', 5, 'http://foo/#5')

        with self.components_with_plugin(status):
            management.call_command('runplugins', stdout=out)

            status.description = 'status description'

            management.call_command('runplugins', stdout=out)
            self.assertIn("Running test Production:Fake plugin", out.getvalue())
            self.assertIn("Updated Fake plugin:Test status", out.getvalue())

            status_model = models.Status.objects.all()[0]
            self.assertEqual(status_model.description, status['description'])
