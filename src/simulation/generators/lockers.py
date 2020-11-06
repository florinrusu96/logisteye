import csv


class LockerScaffold:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long


def generate_lockers(boxes_count):
    return


def read_locker_scaffolds():
    with open('../velib_data.csv') as scaffolds_csv:
        scaffolds_reader = csv.reader(scaffolds_csv)
        for scaffold in scaffolds_reader:
            print(scaffold)



