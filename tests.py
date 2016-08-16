import unittest

from find_combinations import Parser, Matcher, FlightPath


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()


class FlightTestCase(ParserTestCase):
    def test_simple_connect(self):
        f1 = self.parser.parse_line("BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.parser.parse_line("DPS,BNW,2016-10-11T23:08:00,2016-10-12T01:00:00,PV924")

        self.assertTrue(f1.connects_to(f2))

    def test_not_enough_time_does_not_connect(self):
        f1 = self.parser.parse_line("BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.parser.parse_line("DPS,BNW,2016-10-11T22:04:00,2016-10-12T01:00:00,PV924")

        self.assertFalse(f1.connects_to(f2))

    def test_too_much_time_does_not_connect(self):
        f1 = self.parser.parse_line("BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.parser.parse_line("DPS,BNW,2016-10-12T01:05:01,2016-10-12T01:00:00,PV924")

        self.assertFalse(f1.connects_to(f2))


class FlightPathTestCase(ParserTestCase):
    def test_simple_path(self):
        f1 = self.parser.parse_line("BNW,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.parser.parse_line("DPS,BNW,2016-10-11T23:08:00,2016-10-12T01:00:00,PV924")
        f3 = self.parser.parse_line("BNW,HKN,2016-10-12T03:05:01,2016-10-12T05:00:00,PV925")

        path = FlightPath(f1, f2)
        self.assertTrue(path.try_add(f3))
        self.assertEqual(path.get_last_flight(), f3)

    def test_simple_path_repetition(self):
        f1 = self.parser.parse_line("BNW,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.parser.parse_line("DPS,BNW,2016-10-11T23:08:00,2016-10-12T01:00:00,PV924")
        f3 = self.parser.parse_line("BNW,DPS,2016-10-12T03:05:01,2016-10-12T05:00:00,PV925")

        path = FlightPath(f1, f2)
        self.assertFalse(path.try_add(f3))
        self.assertNotEqual(path.get_last_flight(), f3)


class MatcherTestCase(ParserTestCase):
    def test_simple_matcher(self):
        f1 = self.parser.parse_and_add("BNW,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923")
        f2 = self.parser.parse_and_add("DPS,BNW,2016-10-11T23:08:00,2016-10-12T01:00:00,PV924")
        f3 = self.parser.parse_and_add("BNW,HKN,2016-10-12T03:05:01,2016-10-12T05:00:00,PV925")
        f4 = self.parser.parse_and_add("DPS,BNW,2016-10-11T03:05:01,2016-10-11T17:45:00,PV926")

        p1 = FlightPath(f1, f2)
        p2 = FlightPath(f2, f3)
        p3 = FlightPath(f4, f1)

        matcher = Matcher(self.parser.flights)
        matcher.pairing()
        self.assertIn(p1, matcher._paths)
        self.assertIn(p2, matcher._paths)
        self.assertIn(p3, matcher._paths)


if __name__ == '__main__':
    unittest.main()
