#!/usr/bin/env python

import requests
import datetime
import random
import json
import sys
from azure.servicebus import ServiceBusService

sbs = ServiceBusService(service_namespace='chaosMonkeys', shared_access_key_name='RootManageSharedAccessKey', shared_access_key_value=sys.argv[1])

files = ['calculated-bh-sand-conc.json', 'fr-breaker.json', 'slurryrate.json', 'crosslinker.json', 'gelling-agent.json', 'pressure.json', 'surface-sand-conc.json']

pi_data = {}
for datafile in files:
    items = json.load(open('./well-values/' + datafile))
    pi_data[datafile.split('.')[0]] = items['Items']

start = datetime.datetime.now()

#print(pi_data['fr-breaker'])

for i in range(1000):
    row = {'Timestamp': (start + datetime.timedelta(milliseconds=(500*i))).isoformat()}
    for k in pi_data.keys():
        value = random.choice(pi_data[k])
        row[k] = value
    sbs.send_event('fracjob', json.dumps(row))
    #print(row)

