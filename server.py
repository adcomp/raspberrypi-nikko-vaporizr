#!/usr/bin/python

###
#	Python WebSocket Server for Raspberry Pi
#	by David Art <david.madbox@gmail.com>
###

import os
import sys

#import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.escape as escape

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO 4	- RIGHT BACK
# GPIO 17	- RIGHT FORWARD
# GPIO 18	- LEFT BACK
# GPIO 27	- LEFT FORWARD

RIGHT_BACK = 4
RIGHT_FORWARD = 17
LEFT_BACK = 18
LEFT_FORWARD = 27

for outp in (RIGHT_BACK, RIGHT_FORWARD, LEFT_BACK, LEFT_FORWARD):
	GPIO.setup(outp, GPIO.OUT)
	GPIO.output(outp, 0)

def ParseMsg(msg):
	Reset()
	
	if msg == 'POWEROFF':
		ret = os.system('sudo poweroff &')
		sys.exit(0)

  elif msg == 'REBOOT':
    ret = os.system('sudo reboot &')
    sys.exit(0)
	
	elif msg == 'FORWARD':
		print 'FORWARD'
		GPIO.output(LEFT_FORWARD, 1)
		GPIO.output(RIGHT_FORWARD, 1)
	
	elif msg == 'BACK':
		print 'BACK'
		GPIO.output(LEFT_BACK, 1)
		GPIO.output(RIGHT_BACK, 1)
	
	elif msg == 'LEFT_FORWARD':
		print 'LEFT_FORWARD'
		GPIO.output(LEFT_FORWARD, 1)
	
	elif msg == 'LEFT_BACK':
		print 'LEFT_BACK'
		GPIO.output(LEFT_BACK, 1)
	
	elif msg == 'RIGHT_FORWARD':
		print 'RIGHT_FORWARD'
		GPIO.output(RIGHT_FORWARD, 1)
	
	elif msg == 'RIGHT_BACK':
		print 'RIGHT_BACK'
		GPIO.output(RIGHT_BACK, 1)
	
	elif msg == 'LEFT_DONUT':
		print 'LEFT_DONUT'
		GPIO.output(LEFT_FORWARD, 1)
		GPIO.output(RIGHT_BACK, 1)
	
	elif msg == 'RIGHT_DONUT':
		print 'RIGHT_DONUT'
		GPIO.output(LEFT_BACK, 1)
		GPIO.output(RIGHT_FORWARD, 1)

def Reset():
	for outp in (RIGHT_BACK, RIGHT_FORWARD, LEFT_BACK, LEFT_FORWARD):
		GPIO.output(outp, 0)	
	

class WSHandler(tornado.websocket.WebSocketHandler):

	def initialize(self, data):
		self.last_msg = None
		
	def open(self):
		self.connected = True
		print 'new connection'
	  
	def on_message(self, message):
		
		if message == self.last_msg:
			Reset()
			self.last_msg = None
			self.write_message('')
		else:
			ret = ParseMsg(message)
			data = {message: 1}
			self.write_message(escape.json_encode(data))
			self.last_msg = message
 
	def on_close(self):
		self.connected = False
		print 'connection closed'
	  
 
application = tornado.web.Application([
	(r'/piremote', WSHandler, dict(data='')),
])

if __name__ == "__main__":

	application.listen(8888)
	print 'Raspberry Pi - Nikko VaporizR Remote'
	print 'WebSocket Server start ..'
	try:
		ioloop = tornado.ioloop.IOLoop.instance()
		ioloop.start()
	except KeyboardInterrupt:
		print ''
		print 'Keyboard Interrupt.'
		Reset()
		ioloop.stop()
		print 'WebSocket Server stop ..'
		GPIO.cleanup()
	

