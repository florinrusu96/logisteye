from rest_framework import generics

from rest_api import models, serializers


class UserGetView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer