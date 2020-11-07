from rest_framework import generics

from simulation import serializers


class SimulationCreate(generics.CreateAPIView):
    serializer_class = serializers.SimulationSerializer

    def post(self, request, *args, **kwargs):
        #insert data into database manually here and return a 200 response
        pass