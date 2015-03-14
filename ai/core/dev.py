# Rushy Panchal
# ai/core/dev.py

import os
import subprocess

class DevelopmentServer(object):
	'''Mocks a development server for MongoDB and other services'''
	def __init__(self):
		self.running = False
		
		self.mongo = None

	def start(self):
		'''Start all of the server's services'''
		self.devNull = open(os.devnull, "wb")
		self.mongo = subprocess.Popen(["mongod"], stdout = self.devNull)
		
		self.running = True

	def stop(self):
		'''Stop all of the server's services'''
		if self.running:
			self.mongo.kill()
			self.devNull.close()

		self.running = False
