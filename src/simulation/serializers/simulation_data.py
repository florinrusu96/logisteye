from rest_framework import serializers


class FocusPoints(serializers.DictField):
    lat = serializers.FloatField(write_only=True),
    long = serializers.FloatField(write_only=True)


class SimulationSerializer(serializers.Serializer):
    number_of_packages = serializers.IntegerField(write_only=True)
    number_of_couriers = serializers.IntegerField(write_only=True)
    number_of_boxes = serializers.IntegerField(write_only=True)
    focus_points = serializers.ListSerializer(child=FocusPoints())
