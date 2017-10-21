"""Admin classes for defcon.status."""
from django.contrib import admin
from defcon.status import models


@admin.register(models.Component)
class ComponentAdmin(admin.ModelAdmin):
    """Admin for Component."""

    list_display = ('name', 'link', 'contact')


@admin.register(models.Plugin)
class PluginAdmin(admin.ModelAdmin):
    """Admin for Plugin."""

    list_display = ('name', 'link')


@admin.register(models.PluginInstance)
class PluginInstanceAdmin(admin.ModelAdmin):
    """Admin for PluginInstance."""

    list_display = ('name', 'plugin', 'component', 'created_on', 'modified_on')


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin for Status."""

    list_display = ('id', 'title', 'created_on', 'modified_on', 'active')
