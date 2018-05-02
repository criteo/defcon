"""Component commands."""
import logging
import uuid

from django.utils import module_loading
from django.utils import timezone
from django.core.management import base

from defcon.status import models


class Command(base.BaseCommand):
    """Run plugins."""

    help = 'Run pluginss'

    def add_arguments(self, _):
        """Add arguments."""
        pass

    def handle(self, *args, **options):
        """Run the command."""
        # TODO: add filters by components and plugins.

        # Get the status that haven't expired yet to make them expire if
        # they disappeared.
        now = timezone.now()
        existing_statuses = set(models.Status.objects.filter(
            time_end__gte=now).values_list('id', flat=True))
        updated_statuses = set()

        for component_obj in models.Component.objects.all():
            for plugin_obj in component_obj.plugins.all():
                updated_statuses |= self.run_plugin(component_obj, plugin_obj)

        expired_statuses = (existing_statuses - updated_statuses)
        if expired_statuses:
            self.stdout.write(self.style.SUCCESS('Expiring %s' % expired_statuses))
            models.Status.objects.filter(id__in=expired_statuses).update(time_end=now)

    def run_plugin(self, component_obj, plugin_obj):
        """Add a plugin."""
        self.stdout.write('Running %s %s:%s' % (
            plugin_obj.name, component_obj.name, plugin_obj.plugin.name))
        plugin_class = module_loading.import_string(plugin_obj.plugin.py_module)
        plugin = plugin_class(plugin_obj.config)

        try:
            statuses = sorted(plugin.statuses().items())
        except Exception:
            msg = (
                "Failed to run %s:%s" %
                (component_obj.name, plugin_obj.plugin.name))
            logging.exception(msg)
            self.stderr.write(self.style.ERROR(msg))
            plugin_obj.failure += 1
            plugin_obj.failure_on = timezone.now()
            plugin_obj.save()
            return set()

        # Create an identifier unique to this plugin obj.
        statuses = [
            (uuid.uuid5(status_id, str(plugin_obj.id)), status)
            for status_id, status in statuses
        ]

        for status_id, status in statuses:
            self._save_status(plugin_obj, status_id, status)

        plugin_obj.success += 1
        plugin_obj.success_on = timezone.now()
        plugin_obj.save()
        return set([status_id for status_id, _ in statuses])

    def _save_status(self, plugin_obj, status_id, status):
        """Save a status."""
        try:
            del status['id']
            status_obj, created = models.Status.objects.update_or_create(
                id=status_id, defaults=status)

            # Because statuses can be shared between plugins, we always add them
            # to the plugin, not only when they are created.
            plugin_obj.statuses.add(status_obj)
        except Exception:
            msg = "Failed to save status with id #%s" % status_id
            logging.exception(msg)
            self.stderr.write(self.style.ERROR(msg))
        else:
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(
                '%s %s:%s config (%s)' % (action, plugin_obj.plugin.name,
                                          status_obj.title,
                                          status_obj.defcon)))
