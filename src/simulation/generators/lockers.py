import csv
from functools import cmp_to_key
import json
from simulation.generators.utils import *


class LockerScaffold:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    @staticmethod
    def from_scaffold_array(scaffold_array):
        name = scaffold_array[1]
        coordinates = scaffold_array[3]
        [lat, long] = [float(value) for value in coordinates.split(',')]

        return LockerScaffold(name, lat, long)


def check_scaffold_in_useful_area(scaffold):
    return PARIS_LOW_LAT < scaffold.lat < PARIS_HIGH_LAT and PARIS_LOW_LONG < scaffold.long < PARIS_HIGH_LONG


def generate_lockers(boxes_count):
    lockers_count = boxes_count // 3
    scaffolds_array = read_locker_scaffolds()

    # filter data outside area of interest
    scaffolds_array = [scaffold for scaffold in scaffolds_array if check_scaffold_in_useful_area(scaffold)]

    return find_most_appealing(lockers_count, scaffolds_array)


def generate_lockers_json_file(boxes_count):
    lockers = generate_lockers(boxes_count)

    return json.dumps([locker.__dict__ for locker in lockers])


def generate_lockers_csv_file(boxes_count):
    lockers = generate_lockers(boxes_count)
    coordinates = [f"{p.lat},{p.long}" for p in lockers]
    return '\n'.join(coordinates)


def read_locker_scaffolds():
    result = []

    with open('simulation/velib_data.csv') as scaffolds_csv:
        scaffolds_reader = csv.reader(scaffolds_csv, delimiter=';')
        scaffolds_iterator = iter(scaffolds_reader)
        next(scaffolds_iterator)
        for scaffold in scaffolds_iterator:
            result.append(LockerScaffold.from_scaffold_array(scaffold))

    return result


def find_most_appealing(count, scaffolds_array):
    [center_lat, center_long] = compute_center(scaffolds_array)
    comparator = make_comparator_as_distance_to_center(center_lat, center_long)

    sorted_scaffolds = sorted(scaffolds_array,
                              key=cmp_to_key(comparator))
    skip_step = len(sorted_scaffolds) // count

    return [sorted_scaffolds[i * skip_step] for i in range(0, count)]


def compute_center(scaffolds_array):
    lat_values = [scaffold.lat for scaffold in scaffolds_array]
    long_values = [scaffold.long for scaffold in scaffolds_array]

    return [sum(lat_values) / len(lat_values), sum(long_values) / len(long_values)]
