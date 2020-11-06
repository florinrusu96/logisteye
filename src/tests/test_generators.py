import unittest
from simulation.generators import lockers


class LockersGeneratorTest(unittest.TestCase):
    def test_read_scaffolds(self):
        lockers.read_locker_scaffolds()
        self.assertEqual(True, True)

    def test_choose_scaffolds(self):
        result = lockers.generate_lockers(600)
        print(lockers.generate_lockers_json_file(600))
        self.assertEqual(100, len(result))
