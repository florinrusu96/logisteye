from rest_framework import serializers

from rest_api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'password', 'first_name', 'last_name', 'assigned_area')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'first_name': {
                'read_only': True,
            },
            'last_name': {
                'read_only': True
            },
            'assigned_area': {
                'read_only': True
            }
        }
