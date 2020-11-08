import unittest

import pytest

from rest_api.models import Location
from rest_api.routing.routing import *


class RoutingTest(unittest.TestCase):
    def test_compute_point_in_radius(self):
        point1 = Location(latitude=48.7878, longitude=2.42112)
        point2 = Location(latitude=42.5621, longitude=10.2412)

        r = 5

        point_on_radius = compute_point_in_disk(point1, point2, r)
        distance_to_center = compute_distance(point1, point_on_radius)

        self.assertEqual(r, round(distance_to_center))

    def test_apply_distance_in_direction(self):
        point1 = Location(latitude=48.7878, longitude=2.44241)
        desired_distance = 5
        resulting_point_coordinates = apply_distance_to_location(point1.latitude, point1.longitude, 5, 1.71)
        resulting_point = Location(latitude=resulting_point_coordinates[0], longitude=resulting_point_coordinates[1])

        actual_distance = compute_distance(point1, resulting_point)
        self.assertEqual(desired_distance, round(actual_distance))
