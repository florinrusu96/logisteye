from rest_framework import serializers

from rest_api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'assigned_area')
