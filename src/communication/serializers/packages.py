from rest_framework import serializers

from rest_api import models


class PackageListForInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = '__all__'
        depth = 1