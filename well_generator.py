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
    for item in items['Items']:
        dt = item['Timestamp'].split('.')[0]
        if not dt in pi_data:
            pi_data[dt]={}
        pi_data[dt][datafile.split('.')[0]]=item['Value']
    #pi_data[datafile.split('.')[0]] = items['Items']

start = datetime.datetime.now()
#print(pi_data)
json.dump(pi_data,open('/home/chaos/pi_Data.json','w'))

#print(pi_data['fr-breaker'])
for dts in sorted(pi_data.keys()):
    pid=pi_data[dts]
    row = {'Timestamp': (datetime.datetime.now()).isoformat()}
    for k in pid:
        row[k] = pid[k]
    time.sleep(0.5)
    sbs.send_event('fracjob', json.dumps(row))
    #print(row)
    #input()
