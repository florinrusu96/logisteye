from rest_framework import generics, permissions

from rest_api import models, serializers


class PackageListView(generics.ListAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
