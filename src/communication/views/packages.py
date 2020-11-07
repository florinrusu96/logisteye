from rest_framework import generics

from rest_api import models

from communication import serializers


class PackageForInstanceList(generics.ListAPIView):
    # future logic should take into consideration packages that were not delivered
    queryset = models.Package.objects.filter(is_delivered=False)
    serializer_class = serializers.PackageListForInstanceSerializer
    # we should add a permission for is master server
