from rest_framework import serializers
from defcon.status import models


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Component
        fields = '__all__'


class PluginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Plugin
        fields = '__all__'


class PluginInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PluginInstance
        fields = '__all__'


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'
