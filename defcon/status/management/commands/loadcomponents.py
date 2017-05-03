"""Component commands."""
from django.core.management import base
from django.conf import settings

from defcon.status import models


class Command(base.BaseCommand):
    """Load components from settings."""

    help = 'Load components from settings'

    def add_arguments(self, _):
        """Add arguments."""
        pass

    def handle(self, *args, **options):
        """Run the command."""
        existing_components = set(
            models.Component.objects.all().values_list('id', flat=True))
        updated_components = set()

        components = sorted(settings.DEFCON_COMPONENTS.items())
        for cid, component in components:
            self.add_component(cid, component)
            updated_components.add(cid)

        removed_components = existing_components - updated_components
        for cid in removed_components:
            models.Component.objects.filter(id=cid).delete()
            self.stdout.write('Removed %s' % cid)

    def add_component(self, cid, component):
        """Add one component."""
        plugins = component['plugins']
        component = component.copy()
        del component['plugins']

        component_obj, created = models.Component.objects.update_or_create(
            id=cid, defaults=component)

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS('%s %s' % (action, component_obj)))
        component_obj.save()

        existing_plugins = set(
            component_obj.plugins.values_list('name', flat=True))
        updated_plugins = set()

        for plugin_config in plugins:
            plugin_id = plugin_config['plugin']
            name = plugin_config['name']
            description = plugin_config.get('description', '')
            config = plugin_config['config']
            self.configure_plugin(
                component_obj, plugin_id, name, description, config)
            updated_plugins.add(name)

        removed_plugins = existing_plugins - updated_plugins
        for name in removed_plugins:
            component_obj.plugins.filter(name=name).delete()
            self.stdout.write('Removed %s:%s' % (component_obj.name, name))

    def configure_plugin(self, component_obj, plugin_id,
                         name, description, config):
        """Configure a plugin for a component."""
        try:
            plugin_obj = models.Plugin.objects.get(id=plugin_id)
        except models.Plugin.DoesNotExist:
            raise base.CommandError('Plugin "%s" does not exist' % plugin_id)

        defaults = {'description': description, 'config': config}
        pinstance_obj, created = component_obj.plugins.update_or_create(
            plugin=plugin_obj, name=name, defaults=defaults)
        pinstance_obj.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            '%s %s:%s config' % (action, component_obj.name, plugin_obj.name)))
