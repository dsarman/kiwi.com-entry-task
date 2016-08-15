import datetime
import unittest
from find_combinations import Matching, FlightPath, Flight

class FlightPathTestCase(unittest.TestCase):

    def setUp(self):
        self.matcher = Matching()

    def test_simple_return_path(self):
        f1 = self.matcher.parse_line("BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.matcher.parse_line("DPS,BNW,2016-10-11T23:08:00,2016-10-12T01:00:00,PV924")

        self.assertTrue(f1.connects_to(f2))

    def test_not_enough_time_does_not_connect(self):
        f1 = self.matcher.parse_line("BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.matcher.parse_line("DPS,BNW,2016-10-11T22:04:00,2016-10-12T01:00:00,PV924")

        self.assertFalse(f1.connects_to(f2))

    def test_too_much_time_does_not_connect(self):
        f1 = self.matcher.parse_line("BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.matcher.parse_line("DPS,BNW,2016-10-12T01:05:01,2016-10-12T01:00:00,PV924")

        self.assertFalse(f1.connects_to(f2))

if __name__ == '__main__':
    unittest.main()
