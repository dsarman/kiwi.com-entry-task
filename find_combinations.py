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
            if difference > 1 and difference < 4:
                return True
        return False

    def __str__(self, *args, **kwargs):
        return "Flight[source: {}, destination: {}, departure: {}, arrival: {}, flight_number: {}]".format(
            self.source, self.destination, self.departure, self.arrival, self.flight_num)


class Matching:
    def __init__(self, time_format):
        self.time_format = time_format
        self.flights = {}

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

    def parse_and_add(self, line: str):
        self.add_flight(self.parse_line(line))


def main() -> None:
    matcher = Matching("%Y-%m-%dT%H:%M:%S")
    input()  # Skip the first line
    for line in fileinput.input():
        matcher.parse_and_add(line)


if __name__ == "__main__":
    main()
