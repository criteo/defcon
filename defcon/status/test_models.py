from django import test

from defcon.status import models


class ModelTestCase(test.TestCase):
    def test_plugin_instance(self):
        p = models.Plugin.objects.create()
        pi = models.PluginInstance.objects.create(plugin=p)
        self.assertEqual(pi.component, None)
