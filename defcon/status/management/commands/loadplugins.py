"""Component commands."""
from django.utils import module_loading
from django.core.management import base
from django.conf import settings

from defcon.status import models


class Command(base.BaseCommand):
    """Load plugins from settings."""

    help = 'Load plugins from settings'

    def add_arguments(self, _):
        """Add arguments."""
        pass

    def handle(self, *args, **options):
        """Run the command."""
        existing_plugins = set(
            models.Plugin.objects.all().values_list('py_module', flat=True))
        updated_plugins = set()

        plugins = sorted(settings.DEFCON_PLUGINS)
        for py_module in plugins:
            self.add_plugin(py_module)
            updated_plugins.add(py_module)

        removed_plugins = existing_plugins - updated_plugins
        for py_module in removed_plugins:
            models.Plugin.objects.filter(py_module=py_module).delete()
            self.stdout.write('Removed %s' % py_module)

    def add_plugin(self, py_module):
        """Add a plugin."""
        plugin_class = module_loading.import_string(py_module)
        plugin = plugin_class()

        defaults = {
            'id': plugin.short_name,
            'name': plugin.name,
            'description': plugin.description,
            'link': plugin.link,
            'py_module': py_module,
        }
        plugin_obj, created = models.Plugin.objects.update_or_create(
            py_module=py_module, defaults=defaults)

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            '%s %s:%s config' % (action, plugin_obj.name, plugin_obj.py_module)
        ))
