#!/usr/bin/env python

import json
import statistics
import sys

to_parse = sys.argv[1]

f = open(to_parse)
values = []

for item in json.load(f)['Items']:
    values.append(item['Value'])

print("Min: ", min(values))
print("Max: ", max(values))
print("Average: ", sum(values)/len(values))
print("Median: ", statistics.median(values))

