import math
from simulation.generators.constants import *


def compute_distance(lat_1, long_1, lat_2, long_2):
    return math.sqrt((lat_1 - lat_2) ** 2 + (long_1 - long_2) ** 2)


def make_comparator_as_distance_to_center(center_lat, center_long):
    def compare(point_1, point_2):
        diff = compute_distance(point_1.lat, point_1.long, center_lat, center_long) - \
               compute_distance(point_2.lat, point_2.long, center_lat, center_lat)

        return 1 if diff > 0 else -1

    return compare


def apply_distance_to_location(lat, long, lat_dist, long_dist):
    return [
        round(lat + (lat_dist / R_EARTH) * (180 / math.pi), 10),
        round(long + (long_dist / R_EARTH) * (180 / math.pi) / math.cos(lat * math.pi / 180), 10)
    ]
