from rest_framework import serializers

from rest_api import models


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('latitude', 'longitude')
