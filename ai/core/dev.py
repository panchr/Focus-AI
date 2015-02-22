# Rushy Panchal
# ai/core/dev.py

import subprocess

class DevelopmentServer(object):
	'''Mocks a development server for MongoDB and other services'''
	def __init__(self):
		self.running = False
		
		self.mongo = None

	def start(self):
		'''Start all of the server's services'''
		self.mongo = subprocess.Popen(["mongod"])
		
		self.running = True

	def stop(self):
		'''Stop all of the server's services'''
		if self.running:
			self.mongo.kill()

		self.running = False
