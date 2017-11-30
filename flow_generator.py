#!/usr/bin/python3
import requests
import datetime
import random
import json
from azure.servicebus import ServiceBusService


bopd=1062
mcfd=12338
bwpd=3170
pressure=3830
creds=json.load(open('/home/chaos/password.json'))
armageddon=json.load(open('/home/chaos/armageddon.json'))
if not armageddon['state']:
    sbs = ServiceBusService(service_namespace='chaosMonkeys', shared_access_key_name='RootManageSharedAccessKey', shared_access_key_value=creds['password'])


    wells=[{'name':'well1','location':{'lat':36.127927, 'long':-97.678902}, 'multiplier':1},
        {'name':'well2','location':{'lat':36.128802, 'long':-97.681702}, 'multiplier':1.15},
        {'name':'well3','location':{'lat':36.125561, 'long':-97.685328}, 'multiplier':0.75},
        {'name':'well4','location':{'lat':36.124166, 'long':-97.679449}, 'multiplier':1.1},
        {'name':'well5','location':{'lat':36.117974, 'long':-97.680739}, 'multiplier':0.95},
        {'name':'well6okc','location':{'lat':35.490862, 'long':-97.503232}, 'multiplier':0.1}]

    for well in wells:
        row= {'name':well['name'], 'Timestamp':datetime.datetime.now().isoformat()}
        row['location']= "%.5f,%.5f" % (well['location']['lat'],well['location']['long'])
        row['bopd']=bopd*well['multiplier']+random.random()*50
        row['mcfd']=mcfd*well['multiplier']+random.random()*1000
        row['bwpd']=bwpd*well['multiplier']+random.random()*150
        row['pressure']=pressure*well['multiplier']+random.random()*200
        row['location']=well['location']
        sbs.send_event('wellflow', json.dumps(row))
