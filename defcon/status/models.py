import uuid

import jsonfield

from django.db import models
from django.core import validators


class Plugin(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(max_length=254, blank=True)
    url = models.URLField(max_length=254)
    contact = models.EmailField(max_length=254, blank=True)
    py_module = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(
        validators=[
            validators.MaxValueValidator(5),
            validators.MinValueValidator(1)
        ]
    )
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=254, blank=True)
    url = models.URLField(max_length=254)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s - %s' % (
            self.status,
            self.title,
            self.modified_on
        )


class PluginInstance(models.Model):
    plugin = models.ForeignKey(Plugin)
    statuses = models.ManyToManyField(Status, blank=True)
    config = jsonfield.JSONField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    @property
    def component(self):
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
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(max_length=254, blank=True)
    url = models.URLField(max_length=254)
    contact = models.EmailField(max_length=254)
    plugins = models.ManyToManyField(PluginInstance, blank=True)

    def __str__(self):
        return self.name
