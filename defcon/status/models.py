"""Models for defcon.status."""
import uuid
import collections
import datetime

import picklefield.fields as picklefield
import jsonfield

from django.db import models
from django.core import validators
from django.utils import timezone


_ID_VALIDATOR = validators.RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Plugin(models.Model):
    """A defcon plugin."""

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True)
    link = models.URLField(max_length=1024, blank=True)
    py_module = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def _default_time_end():
    return timezone.now() + Status.DEFAULT_ACTIVE_DURATION


class Status(models.Model):
    """A status linked to a plugin instance."""

    # By default statuses are active for 60min
    # Which means that they will not dispear immediately.
    DEFAULT_ACTIVE_DURATION = datetime.timedelta(0, 3600)

    # A stable id for each individual event.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # A defcon status from 5 to 1.
    defcon = models.IntegerField(
        validators=[
            validators.MaxValueValidator(5),
            validators.MinValueValidator(1)
        ],
        default=5
    )
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=1024, blank=True, null=True)
    # To store metadata that will be exposed in the API.
    metadata = jsonfield.JSONField(null=True)
    # Link to the event / documentation.
    link = models.URLField(max_length=1024)
    # Will be used to know if the event is still active or not, useful
    # for scheduled events.
    time_start = models.DateTimeField(auto_now=True)
    time_end = models.DateTimeField(blank=True, null=True,
                                    default=_default_time_end)
    # Set to True if this overrides any over existing status. Useful to
    # force a downgrade of defcon status.
    override = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    @property
    def active(self):
        """Return True if active now."""
        now = timezone.now()
        time_end = self.time_end
        if not time_end:
            time_end = self.time_start + self.DEFAULT_ACTIVE_DURATION
        if now < self.time_start:
            return False
        if now > time_end:
            return False
        return True

    def __str__(self):
        return '%s - %s - %s (active: %s)' % (
            self.defcon,
            self.title,
            self.modified_on,
            self.active
        )

    def save(self, *args, **kwargs):
        """Save the object."""
        if self.time_end is None:
            self.time_end = _default_time_end()
        super(Status, self).save(*args, **kwargs)


class PluginInstance(models.Model):
    """Instance of a plugin (including settings)."""

    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    statuses = models.ManyToManyField(Status, blank=True)
    config = picklefield.PickledObjectField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    success = models.PositiveIntegerField(default=0)
    failure = models.PositiveIntegerField(default=0)
    success_on = models.DateTimeField(null=True, blank=True)
    failure_on = models.DateTimeField(null=True, blank=True)

    @property
    def component(self):
        """Return the component associated with this instance."""
        components = self.component_set.all()
        if not components:
            return None
        return components[0]

    def __str__(self):
        return '%s <Component: %s, Updated: %s>' % (
            self.plugin.name,
            self.component,
            self.modified_on
        )


class Component(models.Model):
    """A monitored component."""

    id = models.CharField(
        primary_key=True, max_length=64, validators=[_ID_VALIDATOR])
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True)
    link = models.URLField(max_length=1024)
    contact = models.EmailField(max_length=254)
    plugins = models.ManyToManyField(PluginInstance, blank=True)

    def all_statuses(self):
        """Return all statuses for a component."""
        for plugin in self.plugins.all():
            for status in plugin.statuses.all():
                yield status

    def statuses(self, defcon=None):
        """Return statuses for a specific defcon level."""
        if defcon is None:
            defcon = self.defcon

        ret = []
        for status in self.all_statuses():
            if not status.active:
                continue
            if defcon != status.defcon:
                continue
            ret.append(status)

        return ret

    def statuses_by_plugins(self):
        """Return all statuses indexed by defcon number."""
        ret = {}
        defcons = [5, 4, 3, 2, 1]

        for dc in defcons:
            ret[dc] = collections.defaultdict(list)

        for plugin in self.plugins.all():
            for status in plugin.statuses.all():
                if status.active:
                    ret[status.defcon][plugin].append(status)

        for dc in defcons:
            ret[dc].default_factory = None

        ret = sorted(ret.items(), key=lambda i: i[0])
        ret.reverse()

        return ret

    @property
    def defcon(self):
        """Return defcon number."""
        defcon = 5
        override = False
        for status in self.all_statuses():
            if not status.active:
                continue
            if status.override:
                # If it's the first override, reset defcon.
                if override is False:
                    defcon = status.defcon
                    override = True
            else:
                # If there is an override, account only overrides.
                if override is True:
                    continue

            # Else, always take the minimum.
            defcon = min(status.defcon, defcon)

        return defcon

    def __str__(self):
        return self.name
