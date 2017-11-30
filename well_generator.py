#!/usr/bin/python3

import requests
import datetime
import random
import json
import sys
import os
import time

from azure.servicebus import ServiceBusService

creds=json.load(open('/home/chaos/password.json'))

sbs = ServiceBusService(service_namespace='chaosMonkeys', shared_access_key_name='RootManageSharedAccessKey', shared_access_key_value=creds['password'])

files = ['calculated-bh-sand-conc.json', 'fr-breaker.json', 'slurryrate.json', 'crosslinker.json', 'gelling-agent.json', 'pressure.json', 'surface-sand-conc.json']

pi_data = {}
max=0
for datafile in files:
    fn = os.path.join(os.path.dirname(__file__), 'well-values/' + datafile)
    items = json.load(open(fn))
    pi_data[datafile.split('.')[0]] = items['Items']

start = datetime.datetime.now()

#print(pi_data['fr-breaker'])

for i in range(1000):
    row = {'Timestamp': (start + datetime.timedelta(milliseconds=(500*i))).isoformat()}
    for k in pi_data.keys():
        value = pi_data[k][i]['Value']
        row[k] = value
    time.sleep(0.5)
    sbs.send_event('fracjob', json.dumps(row))
    #print(row)
    #input()

