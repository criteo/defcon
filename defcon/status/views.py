from django.shortcuts import render

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
