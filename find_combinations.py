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


flights_from = {}

time_format_string = "%Y-%m-%dT%H:%M:%S"

def parse_line(line: str) -> Flight:
    split_line = line.rstrip("\n").split(",")
    departure = datetime.datetime.strptime(split_line[2], time_format_string)
    arrival = datetime.datetime.strptime(split_line[3], time_format_string)
    new_flight = Flight(split_line[0], split_line[1], departure, arrival, split_line[4])
    return new_flight


def main() -> None:
    input()  # Skip the first line
    for line in fileinput.input():
        print(parse_line(line))


if __name__ == "__main__":
    main()
