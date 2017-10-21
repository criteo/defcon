"""Views of defcon.status."""
from django import shortcuts

from annoying import decorators as an_decorators
from rest_framework import viewsets
from rest_framework import permissions

from defcon.status import models
from defcon.status import serializers


class DefConViewSet(viewsets.ReadOnlyModelViewSet):
    """API view for Component with expanded statuses."""

    queryset = models.Component.objects.all()
    serializer_class = serializers.ComponentFullSerializer


class SimpleViewSet(viewsets.ReadOnlyModelViewSet):
    """API view for Component with expanded statuses."""

    queryset = models.Component.objects.all()
    serializer_class = serializers.ComponentSimpleSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    """API view for Component."""

    queryset = models.Component.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ComponentSerializer


class PluginViewSet(viewsets.ModelViewSet):
    """API view for Plugin."""

    queryset = models.Plugin.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PluginSerializer


class PluginInstanceViewSet(viewsets.ModelViewSet):
    """API view for PluginInstance."""

    queryset = models.PluginInstance.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PluginInstanceSerializer


class StatusViewSet(viewsets.ModelViewSet):
    """API view for Status."""

    queryset = models.Status.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.StatusSerializer


@an_decorators.render_to('index.html')
def index(request):
    """Show the list of components."""
    components = models.Component.objects.all()
    return {'components': components}


@an_decorators.render_to('status.html')
def status(request, component_id):
    """Display a specific component."""
    component = shortcuts.get_object_or_404(models.Component, pk=component_id)
    base_url = "{0}://{1}".format(request.scheme, request.get_host())
    return {'component': component, 'base_url': base_url}


@an_decorators.render_to('badge.svg', content_type="image/svg+xml")
def badge(request, component_id):
    """Display a badge for a specific component."""
    component = shortcuts.get_object_or_404(models.Component, pk=component_id)
    return {'component': component}
