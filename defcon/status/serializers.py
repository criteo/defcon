from rest_framework import serializers
from defcon.status import models


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Component
        fields = ('name', 'description', 'url', 'contact')
        #fields = '__all__'
