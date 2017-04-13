from django.contrib import admin
from defcon.status import models


@admin.register(models.Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'contact')


@admin.register(models.Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'contact')


@admin.register(models.PluginInstance)
class PluginInstanceAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'component', 'created_on', 'modified_on')



@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_on', 'modified_on')

