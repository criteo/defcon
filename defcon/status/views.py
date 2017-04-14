from django import shortcuts

from annoying import decorators as an_decorators
from rest_framework import viewsets
from rest_framework import permissions

from defcon.status import models
from defcon.status import serializers


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = models.Component.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ComponentSerializer


class PluginViewSet(viewsets.ModelViewSet):
    queryset = models.Plugin.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PluginSerializer


class PluginInstanceViewSet(viewsets.ModelViewSet):
    queryset = models.PluginInstance.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PluginInstanceSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.StatusSerializer


@an_decorators.render_to('index.html')
def index(request):
    components = models.Component.objects.all()
    return {'components': components}


@an_decorators.render_to('status.html')
def status(request, component_id):
    component = shortcuts.get_object_or_404(models.Component, pk=component_id)
    print (component)
    return {'component': component}

