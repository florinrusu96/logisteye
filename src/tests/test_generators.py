import unittest
from simulation.generators import lockers
from simulation.generators import packages


class LockersGeneratorTest(unittest.TestCase):
    def test_read_scaffolds(self):
        lockers.read_locker_scaffolds()
        self.assertEqual(True, True)

    def test_choose_scaffolds(self):
        result = lockers.generate_lockers(600)
        print(lockers.generate_lockers_json_file(600))
        print(lockers.generate_lockers_csv_file(60))
        self.assertEqual(200, len(result))

    def test_paris_bounds(self):
        all_lockers = lockers.read_locker_scaffolds()
        lat_array = [locker.lat for locker in all_lockers]
        long_array = [locker.long for locker in all_lockers]

        print(f"({min(lat_array)}, {min(long_array)}); ({max(lat_array)}, {max(long_array)})")
        self.assertEqual(True, True)


class PackagesGeneratorTest(unittest.TestCase):
    def test_generate_packages(self):
        result = packages.generate_packages(200)
        # print(result)
        self.assertEqual(200, len(result))

    def test_generate_squares(self):
        result_json = packages.group_in_squares_json(packages.generate_packages(
            3500, [(48.8718468, 2.3665066), (48.8263230, 2.2876292)]), 0.3)
        # print(result)
        print(result_json)
        self.assertEqual(True, True)
