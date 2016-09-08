#!/usr/bin/env python3
import argparse
import copy
import datetime
import sys
from typing import List, Set


class Flight:
    """
    Class representation of one flight information.
    """

    def __init__(self, source: str, destination: str, departure: datetime.datetime, arrival: datetime.datetime,
                 flight_num: str) -> None:
        self.source = source
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.flight_num = flight_num

    def connects_to(self, flight) -> bool:
        """
        Test if this flight connects to the given one.
        """
        if self.destination == flight.source:
            difference = flight.departure - self.arrival
            if difference.total_seconds() >= 3600 and difference.total_seconds() <= 14400:
                return True
        return False

    def __str__(self):
        return "Flight[source: {}, destination: {}, departure: {}, arrival: {}, flight_number: {}]".format(
            self.source, self.destination, self.departure, self.arrival, self.flight_num)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.flight_num == other.flight_num)

    def __hash__(self):
        return hash(self.flight_num)


class FlightPath:
    def __init__(self, flight_one: Flight, flight_two: Flight):
        assert flight_one.connects_to(flight_two), "Flights must connect"
        self.path = [flight_one, flight_two]

    def try_add(self, flight: Flight) -> bool:
        """
        Tries to add given flight to the flight path.
        Checks for repeating paths A -> B -> A -> B.
        """
        last_path_index = len(self.path) - 1
        if not self.path[last_path_index].connects_to(flight):
            return False

        for i in range(0, last_path_index + 1):
            existing_destination = self.path[i].destination
            existing_source = self.path[i].source
            if existing_destination == flight.destination and existing_source == flight.source:
                return False
        self.path.append(flight)
        return True

    def get_last_flight(self):
        """
        Returns last flight in path.
        """
        return self.path[len(self.path) - 1]

    def get_output_str(self):
        """
        Returns concise string representation of flight path.
        """
        out_str = ""
        path_size = len(self.path)
        for i in range(0, path_size):
            out_str += self.path[i].flight_num
            if i == path_size - 1:
                out_str += "\n"
            else:
                out_str += ","
        return out_str

    def __str__(self):
        out = self.path[0].source
        path_size = len(self.path)
        for i in range(0, path_size):
            out += "-- " + self.path[i].flight_num + " -->" + self.path[i].destination
        return out

    def __len__(self):
        return len(self.path)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        size = len(self.path)
        if size != len(other.path):
            return False
        for i in range(0, size):
            if not self.path[i] == other.path[i]:
                return False
        return True

    def __hash__(self):
        hash_val = hash(self.path[0])
        for i in range(1, len(self.path)):
            hash_val += hash(self.path[i])
        return hash_val


class Parser:
    def __init__(self, time_format: str = "%Y-%m-%dT%H:%M:%S"):
        self.time_format = time_format
        self.flights = []
        self.flights_count = 0

    def parse_file(self, parse_all=False, file=None):
        """
        Parses given file, or stdout if none is supplied.
        :param ignore_first: If True, ignores first line
        """
        if not parse_all:
            input()
        for line in sys.stdin:
            self.parse_and_add(line)

    def parse_line(self, line: str) -> Flight:
        """
        Parses one line of csv formatted input.
        :return: Flight object with the parsed data.
        """
        split_line = line.rstrip("\n").split(",")
        departure = datetime.datetime.strptime(split_line[2], self.time_format)
        arrival = datetime.datetime.strptime(split_line[3], self.time_format)
        new_flight = Flight(split_line[0], split_line[1], departure, arrival, split_line[4])
        return new_flight

    def parse_and_add(self, line: str) -> Flight:
        """
        Parses and adds given line.
        """
        flight = self.parse_line(line)
        self.add_flight(flight)
        return flight

    def add_flight(self, flight: Flight):
        """
        Adds flight into the flights list.
        Used in testing.
        """
        self.flights.append(flight)


class Matcher:
    def __init__(self, data: List[Flight]):
        self.data = data
        self._paths = []

    def pairing(self):
        """
        Does one round of pairing between flights.
        Creates new flight paths, or appends to existing ones.
        """
        if len(self._paths) == 0:
            second_values = self.data
            get_flight = lambda x: x
            first = True
        else:
            second_values = self._paths
            get_flight = lambda x: x.get_last_flight()
            first = False

        for value in second_values:
            f1 = get_flight(value)
            for f2 in self.data:
                if f1.connects_to(f2):
                    if first:
                        self._paths.append(FlightPath(f1, f2))
                    else:
                        path_copy = copy.copy(value)
                        added = path_copy.try_add(f2)
                        if added:
                            self._paths.append(path_copy)

    def get_paths(self) -> Set[FlightPath]:
        return set(self._paths)

    def full_pairing(self):
        for i in range(0, len(self.data)):
            self.pairing()

    def write_to_stdout(self):
        for path in self.get_paths():
            sys.stdout.write(path.get_output_str())


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Find connecting flights.")
    arg_parser.add_argument('-a', dest="parse_all", action="store_true", help="Do not ignore first line of input.")
    args = arg_parser.parse_args()
    parser = Parser()
    parser.parse_file(args.parse_all)
    matcher = Matcher(parser.flights)
    matcher.full_pairing()
    matcher.write_to_stdout()


if __name__ == "__main__":
    main()
