#! /usr/bin/env python

import cherrypy
import pusher
from twilio import twiml
import urllib


pusher_appid = ''
pusher_key = ''
pusher_secret = ''

class Start(object):
	def call(self, var=None, **params):
		r = twiml.Response()
		r.say("Record your message after the beep")
		r.record(action="/record")
		return str(r)
	def record(self, var=None, **params):
		url = urllib.unquote(cherrypy.request.params['RecordingUrl'])
		print url
		p = pusher.Pusher(app_id=pusher_appid, key=pusher_key, secret=pusher_secret)
		p['airpage'].trigger('message', {'url': url})
		r = twiml.Response()
		r.say("Your message has been sent")
		return str(r)
	call.exposed = True
	record.exposed = True


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 9000
cherrypy.quickstart(Start())
