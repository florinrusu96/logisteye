from rest_framework import serializers

from rest_api import models


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = ('location_center', 'radius')
        depth = 1
