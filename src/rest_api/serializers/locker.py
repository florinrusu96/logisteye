from rest_framework import serializers

from rest_api import models


class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Locker
        fields = ('location', 'owner')
        depth = 1
