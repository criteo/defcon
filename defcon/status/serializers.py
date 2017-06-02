"""Serializers for defcon.status."""
from rest_framework import serializers
from defcon.status import models


# Models for the full API.

class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Component."""

    class Meta:
        """Configuration."""

        model = models.Component
        fields = '__all__'


class ComponentSimpleSerializer(ComponentSerializer):
    """Serializer for Component."""

    class Meta(ComponentSerializer.Meta):
        """Configuration."""

        fields = ['name', 'contact', 'link', 'defcon', 'description']


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


# Bellow are serializers for the simple /defcon/ API.


class PluginInstanceFullSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for PluginInstance with expanded content."""

    statuses = StatusSerializer(many=True)

    class Meta:
        """Configuration."""

        model = models.PluginInstance
        fields = '__all__'


class ComponentFullSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Component with expanded content."""

    plugins = PluginInstanceFullSerializer(many=True)

    # Statuses for current defcon level.
    statuses = StatusSerializer(many=True)
    defcon = serializers.IntegerField()

    class Meta:
        """Configuration."""

        model = models.Component
        fields = '__all__'
