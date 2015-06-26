#!/usr/bin/env python3
"""IP Overlap Script.

This script ``flattens`` the overlapping IP ranges
producing the non-overlapping ranges.

For the following input:

    1.1.1.1,10.10.10.10,US,T-Mobile
    2.2.2.2,3.3.3.3,US,Sprint
    5.5.5.5,8.8.8.8,AU,Telstra
    6.6.6.6,7.7.7.7,AU,voda AU

the script will produce the following output:

    1.1.1.1,2.2.2.1,US,T-Mobile
    2.2.2.2,3.3.3.3,US,Sprint
    3.3.3.4,5.5.5.4,US,T-Mobile
    5.5.5.5,6.6.6.5,AU,Telstra
    6.6.6.6,7.7.7.7,AU,voda AU
    7.7.7.8,8.8.8.8,AU,Telstra
    8.8.8.9,10.10.10.10,US,T-Mobile

"""

import fileinput
import csv
import sys

from ipaddress import ip_address

START_POINT = 1
END_POINT = 0


def make_points(reader):
    """Make the list of points from the CSV."""
    points = []
    for row in reader:
        points.append((ip_address(row['start']), START_POINT, row['id']))
        points.append((ip_address(row['end']), END_POINT, row['id']))
    return sorted(points)


def make_ranges(points):
    """Make the list of non-overlapping flattened ranges."""
    ranges = []
    current_id = []
    last_start = None

    for offset, marker, net_id in points:
        if marker == START_POINT:
            if last_start is not None:
                country, cell = current_id[-1]
                ranges.append((last_start, offset - 1, country, cell))
            current_id.append(net_id)
            last_start = offset
        elif marker == END_POINT:
            country, cell = current_id[-1]
            ranges.append((last_start, offset, country, cell))
            current_id.pop()
            last_start = offset + 1

    return ranges


def to_csv(ranges):
    """Write CSV to stdout."""
    writer = csv.writer(sys.stdout)
    writer.writerows(ranges)


def main():
    """Script entry point."""
    with fileinput.input() as csvfile:
        fieldnames = ('start', 'end')
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, restkey='id')

        points = make_points(reader)
        ranges = make_ranges(points)
        to_csv(ranges)

if __name__ == '__main__':
    main()
