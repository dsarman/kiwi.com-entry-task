#!/usr/bin/env python3
import fileinput
import datetime


class Flight:
    def __init__(self, source: str, destination: str, departure: datetime.datetime, arrival: datetime.datetime,
                 flight_num: str) -> None:
        self.source = source
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.flight_num = flight_num

    def connects_to(self, flight) -> bool:
        if self.destination == flight.source:
            difference = self.arrival - flight.departure
            if difference.total_seconds() > 3600 and difference.total_seconds() < 14400:
                return True
        return False

    def __str__(self, *args, **kwargs):
        return "Flight[source: {}, destination: {}, departure: {}, arrival: {}, flight_number: {}]".format(
            self.source, self.destination, self.departure, self.arrival, self.flight_num)


class Matching:
    def __init__(self, time_format):
        self.time_format = time_format
        self.flights = {}
        self.flights_count = 0

    def parse_line(self, line: str) -> Flight:
        split_line = line.rstrip("\n").split(",")
        departure = datetime.datetime.strptime(split_line[2], self.time_format)
        arrival = datetime.datetime.strptime(split_line[3], self.time_format)
        new_flight = Flight(split_line[0], split_line[1], departure, arrival, split_line[4])
        return new_flight

    def add_flight(self, flight: Flight) -> None:
        existing_flights = self.flights.get(flight.source)
        if existing_flights is not None:
            existing_flights.append(flight)
        else:
            existing_flights = [flight]
        self.flights[flight.source] = existing_flights
        self.flights_count += 1

    def parse_and_add(self, line: str) -> None:
        self.add_flight(self.parse_line(line))


class FlightPath:
    def __init__(self, flight_one, flight_two):
        self.path = [flight_one, flight_two]

    def try_add(self, flight: Flight) -> bool:
        path_size = len(self.path)
        if not self.path[path_size].connects_to(flight):
            return False

        for i in range(0, path_size - 1):
            existing_destination = self.path[i].destination
            existing_source = self.path[i+1].source
            if existing_destination == self.path[path_size].destination and existing_source == flight.source:
                return False
        self.path.append(flight)
        return True

    def __str__(self, *args, **kwargs):
        out = self.path[0].source
        path_size = len(self.path)
        for i in range(1,path_size):
            out +=  "-- " + self.path[i].flight_num + " -->" + self.path[i].destination
        return out


def main() -> None:
    matcher = Matching("%Y-%m-%dT%H:%M:%S")
    input()  # Skip the first line
    for line in fileinput.input():
        matcher.parse_and_add(line)

    paths = []

    for key, flights in matcher.flights.items():
        for key2, flights2 in matcher.flights.items():
            if key != flights2[0].destination:
                for f1 in flights:
                    for f2 in flights2:
                        if f1.connects_to(f2):
                            paths.append(FlightPath(f1, f2))

    for path in paths:
        print(path)




if __name__ == "__main__":
    main()
