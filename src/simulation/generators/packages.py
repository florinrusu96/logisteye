import random


PARIS_LOW_LAT = 48.7646675418
PARIS_LOW_LONG = 2.16559678316

PARIS_HIGH_LAT = 48.9470224368
PARIS_HIGH_LONG = 2.53824211657


def generate_packages(count):
    lat_array = [round(random.uniform(PARIS_LOW_LAT, PARIS_HIGH_LAT), 10) for i in range(0, count)]
    long_array = [round(random.uniform(PARIS_LOW_LONG, PARIS_HIGH_LONG), 10) for i in range(0, count)]

    return [(lat_array[i], long_array[i]) for i in range(0, count)]
