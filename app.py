import cherrypy
import os
from cherrypy.process import servers
import pusher
from twilio import twiml
import urllib


pusher_appid = 'PUSHER_APPID' in os.environ
pusher_key = 'PUSHER_KEY' in os.environ
pusher_secret = 'PUSHER_SECRET' in os.environ

def fake_wait_for_occupied_port(host, port): 
	return

servers.wait_for_occupied_port = fake_wait_for_occupied_port

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

cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.quickstart(Start())