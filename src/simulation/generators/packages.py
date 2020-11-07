import random
import json
from functools import cmp_to_key

from simulation.generators.utils import *

PARIS_LOW_LAT = 48.8145700
PARIS_LOW_LONG = 2.2684700

PARIS_HIGH_LAT = 48.9060200
PARIS_HIGH_LONG = 2.4225900

R_EARTH = 6378


def get_focused_range(point, focus_weight):
    focus_lat_diff = (PARIS_HIGH_LAT - PARIS_LOW_LAT) / focus_weight
    focus_long_diff = (PARIS_HIGH_LONG - PARIS_LOW_LONG) / focus_weight

    low_lat = max(point[0] - focus_lat_diff, PARIS_LOW_LAT)
    high_lat = min(point[0] + focus_lat_diff, PARIS_HIGH_LAT)

    low_long = max(point[1] - focus_long_diff, PARIS_LOW_LONG)
    high_long = min(point[1] + focus_long_diff, PARIS_HIGH_LONG)
    return [(low_lat, low_long), (high_lat, high_long)]


def generate_packages(count, focus_points=None):
    if focus_points is None:
        focus_points = []
    splits = 1 + len(focus_points)

    lat_array = [round(random.uniform(PARIS_LOW_LAT, PARIS_HIGH_LAT), 10) for i in range(0, count // splits)]
    long_array = [round(random.uniform(PARIS_LOW_LONG, PARIS_HIGH_LONG), 10) for i in range(0, count // splits)]

    if splits == 1:
        return [(lat_array[i], long_array[i]) for i in range(0, count)]

    for focus in focus_points[:-1]:
        focused_range = get_focused_range(focus, 3 * splits)
        lat_array.extend([round(random.uniform(focused_range[0][0], focused_range[1][0]), 10)
                          for i in range(0, count // splits)])
        long_array.extend([round(random.uniform(focused_range[0][1], focused_range[1][1]), 10)
                          for i in range(0, count // splits)])

    focused_range = get_focused_range(focus_points[-1], splits)
    lat_array.extend([round(random.uniform(focused_range[0][0], focused_range[1][0]), 10)
                      for i in range(len(lat_array), count)])
    long_array.extend([round(random.uniform(focused_range[0][1], focused_range[1][1]), 10)
                      for i in range(len(long_array), count)])

    return [(lat_array[i], long_array[i]) for i in range(0, count)]


def group_in_squares(packages, km):
    average_lat = (PARIS_LOW_LAT + PARIS_HIGH_LAT) / 2
    average_long = (PARIS_LOW_LONG + PARIS_HIGH_LONG) / 2

    square_in_the_middle = compute_square_by_middle_and_dimension(average_lat, average_long, km)
    rectangle_creator = MapRectanglesCreator(packages, square_in_the_middle, km)
    return rectangle_creator.fill_squares_array()


def group_in_squares_json(packages, km):
    squares = group_in_squares(packages, km)
    return json.dumps([square.to_map() for square in squares])


def compute_square_by_middle_and_dimension(lat_mid, long_mid, km):
    half_dimension = km / 2

    return [
        apply_distance_to_location(lat_mid, long_mid, -half_dimension, -half_dimension),
        apply_distance_to_location(lat_mid, long_mid, -half_dimension, half_dimension),
        apply_distance_to_location(lat_mid, long_mid, half_dimension, half_dimension),
        apply_distance_to_location(lat_mid, long_mid, half_dimension, -half_dimension)
    ]


def apply_distance_to_location(lat, long, lat_dist, long_dist):
    return [
        round(lat + (lat_dist / R_EARTH) * (180 / math.pi), 10),
        round(long + (long_dist / R_EARTH) * (180 / math.pi) / math.cos(lat * math.pi / 180), 10)
    ]


def get_square_center(square, dimension):
    half_dimension = dimension / 2
    return apply_distance_to_location(square[0][0], square[0][1], half_dimension, half_dimension)


class MapRectanglesCreator:
    def __init__(self, packages, center_square, square_dimension):
        self.packages = [PointDefinition(package[0], package[1]) for package in packages]
        self.absolute_center = get_square_center(center_square, square_dimension)
        self.square_dimension = square_dimension
        self.visited_squares = []
        self.visited_positions = []

    def fill_squares_array(self):
        comparator = make_comparator_as_distance_to_center(self.absolute_center[0], self.absolute_center[1])
        self.packages = sorted(self.packages, key=cmp_to_key(comparator), reverse=True)

        self.fill_squares_array_recursive([0, 0])

        return self.visited_squares

    def extract_packages_in_square(self, square):
        result = []
        for package in self.packages:
            if self.fits_square(square, package):
                self.packages.remove(package)
                result.append(package)

        return result

    def fill_squares_array_recursive(self, current_position):
        if current_position in self.visited_positions:
            return
        current_square_center = apply_distance_to_location(self.absolute_center[0], self.absolute_center[1],
                                                           current_position[0] * self.square_dimension,
                                                           current_position[1] * self.square_dimension)
        current_square = compute_square_by_middle_and_dimension(current_square_center[0], current_square_center[1],
                                                                self.square_dimension)

        if current_square[0][0] > PARIS_HIGH_LAT or current_square[0][1] > PARIS_HIGH_LONG:
            return

        if current_square[2][0] < PARIS_LOW_LAT or current_square[2][1] < PARIS_LOW_LONG:
            return

        packages_in_square = self.extract_packages_in_square(current_square)
        packages_in_square_count = len(packages_in_square)

        if packages_in_square_count == 0:
            color = "green"
        elif packages_in_square_count < 5:
            color = "yellow"
        elif packages_in_square_count < 10:
            color = "orange"
        else:
            color = "red"

        self.visited_squares.append(SquareDefinition([
            PointDefinition(current_square[0][0], current_square[0][1]),
            PointDefinition(current_square[1][0], current_square[1][1]),
            PointDefinition(current_square[2][0], current_square[2][1]),
            PointDefinition(current_square[3][0], current_square[3][1]),
        ], color))
        self.visited_positions.append(current_position)

        self.fill_squares_array_recursive(self.get_position_above(current_position))
        self.fill_squares_array_recursive(self.get_position_below(current_position))
        self.fill_squares_array_recursive(self.get_position_left(current_position))
        self.fill_squares_array_recursive(self.get_position_right(current_position))

    @staticmethod
    def get_position_above(position):
        return [position[0], position[1] + 1]

    @staticmethod
    def get_position_below(position):
        return [position[0], position[1] - 1]

    @staticmethod
    def get_position_left(position):
        return [position[0] - 1, position[1]]

    @staticmethod
    def get_position_right(position):
        return [position[0] + 1, position[1]]

    @staticmethod
    def fits_square(square, point):
        return square[0][0] < point.lat < square[2][0] and square[0][1] < point.long < square[2][1]


class PointDefinition:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long


class SquareDefinition:
    def __init__(self, corners, color):
        self.corners = corners
        self.color = color

    def to_map(self):
        return {"color": self.color, "corners": [point.__dict__ for point in self.corners]}
