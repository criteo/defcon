"""Serializers for defcon.status."""
from rest_framework import serializers
from defcon.status import models


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Component."""

    class Meta:
        """Configuration."""

        model = models.Component
        fields = '__all__'


class PluginSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Plugin."""

    class Meta:
        """Configuration."""

        model = models.Plugin
        fields = '__all__'


class PluginInstanceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for PluginInstance."""

    class Meta:
        """Configuration."""

        model = models.PluginInstance
        fields = '__all__'


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Status."""

    class Meta:
        """Configuration."""

        model = models.Status
        fields = '__all__'
