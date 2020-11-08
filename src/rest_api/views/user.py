from django.core import exceptions
from rest_framework import generics, response, status

from rest_api import models, serializers


class UserPostView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        try:
            user = models.User.objects.get(email=serializer.data['email'])
        except exceptions.ObjectDoesNotExist:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = serializers.UserSerializer(user)
            return response.Response(data=serializer.data)
