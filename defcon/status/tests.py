from django import test

from defcon.status import models
from defcon.status import views


class ModelTestCase(test.TestCase):
    def test_plugin_instance(self):
        p = models.Plugin.objects.create()
        pi = models.PluginInstance.objects.create(plugin=p)
        self.assertEqual(pi.component, None)


class ViewTestcase(test.TestCase):
    def test_component_view_set(self):
        views.ComponentViewSet()
