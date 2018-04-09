"""Defcon metrics."""

import time
import prometheus_client

from django.conf import settings
from defcon.status import models


class DefconCollector(object):
    """Collector to export defcon metrics."""

    def __init__(self, registry=prometheus_client.REGISTRY):
        """Create a new defcon collector."""
        self._first = True
        if registry:
            registry.register(self)

    def collect(self):
        """Collect all metrics."""
        if self._first:
            # Avoid collecting when running from manage.py.
            self._first = False
            return []

        metrics = []

        defcon = prometheus_client.core.GaugeMetricFamily(
            "defcon", "defcon status for a component", labels=['component']
        )
        for component in models.Component.objects.all():
            defcon.add_metric([component.id], component.defcon)
        metrics.append(defcon)

        labels = ['id', 'name']
        success_on = prometheus_client.core.GaugeMetricFamily(
            "plugin_success_on", "Last success for this plugin", labels=labels
        )
        failure_on = prometheus_client.core.GaugeMetricFamily(
            "plugin_failure_on", "Last failure for this plugin", labels=labels
        )
        success = prometheus_client.core.CounterMetricFamily(
            "plugin_success_total", "Success counter per plugin", labels=labels
        )
        failure = prometheus_client.core.CounterMetricFamily(
            "plugin_failure_total", "failure counter per plugin", labels=labels
        )
        for plugin in models.PluginInstance.objects.all():
            labels = [str(plugin.id), plugin.name]
            timestamp = time.mktime(plugin.success_on.timetuple()) if plugin.success_on else 0
            success_on.add_metric(labels, timestamp)
            timestamp = time.mktime(plugin.failure_on.timetuple()) if plugin.failure_on else 0
            failure_on.add_metric(labels, timestamp)
            success.add_metric(labels, plugin.success)
            failure.add_metric(labels, plugin.failure)
        metrics.extend([success_on, failure_on, success, failure])

        return metrics


if getattr(settings, 'DEFCON_METRICS', False):
    DEFCON_COLLECTOR = DefconCollector()
