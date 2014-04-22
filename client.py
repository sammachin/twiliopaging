#!/usr/bin/env python

import pusherclient
import json
from soco import SoCo
from soco import SonosDiscovery
import time

global pusher

pusher_key = ''

def connect_handler(data):
    channel = pusher.subscribe('airpage')
    channel.bind('message', callback)

def callback(d):
	data = json.loads(d)
	url = data['url']
	sonos_devices = SonosDiscovery()
	ips = sonos_devices.get_speaker_ips()
	master = SoCo(ips[0])
	masteruid = master.get_speaker_info()['uid']
	for ip in ips:
	            if not (ip == master.speaker_ip):
	                slave = SoCo(ip)
	                ret = slave.join(masteruid)
	oldvol = master.volume
	master.volume = 60
	master.play_uri(url)
	playing = True
	while playing:
		if master.get_current_transport_info()['current_transport_state'] == 'STOPPED':
			playing = False
	master.volume = oldvol		
	for ip in ips:
		if not (ip == master.speaker_ip):
			slave = SoCo(ip)
			slave.unjoin()



pusher = pusherclient.Pusher(pusher_key)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    time.sleep(1)