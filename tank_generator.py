#!/usr/bin/python3
import requests
import datetime
import random
import json
from azure.servicebus import ServiceBusService
creds=json.load(open('/home/chaos/password.json'))
armageddon=json.load(open('/home/chaos/armageddon.json'))

if not armageddon['state']:
    sbs = ServiceBusService(service_namespace='chaosMonkeys', shared_access_key_name='RootManageSharedAccessKey', shared_access_key_value=creds['password'])

    min_level=5.656
    max_level=13.563
    cl=json.load(open('/home/chaos/tank_stat.json','r'))

    row= {'name':'StackTank', 'Timestamp':datetime.datetime.now().isoformat(), 'location':{'lat':36.116626,'long':-97.709833},'max':max_level}
    cl['level']+=(random.random()/10)    
    if cl['level']>max_level:
        cl['level']=min_level
    row['level']=cl['level']
    json.dump(cl,open('/home/chaos/tank_stat.json','w'))
    sbs.send_event('tanklevel', json.dumps(row))
