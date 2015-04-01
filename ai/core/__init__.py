# Rushy Panchal
# ai/core/__init__.py

import core
import models

import threading
import signal
import time
import sys
import os
import zmq

import config

def start():
	'''Starts the core features'''
	app = Application()
	app.run()
	return app

class Application(object):
	'''Houses the entire application'''
	def __init__(self, devMode = False):
		self.devServer = core.dev.DevelopmentServer() if (devMode or config.DEV_MODE) else None
		self.db = None
		self.server = None
		self.engine = None
		self.handler = None
		self.serverThread = None

	def run(self):
		'''Runs the application'''
		if self.devServer:
			self.devServer.start()

		self.db = core.database.Database(host = config.DB_HOST, port = config.DB_PORT)
		self.db.register([
			models.User,
			models.Rule,
			models.Game
			])
		models.register(self.db)

		self.engine = core.engine.Engine(database = self.db)

		self.server = core.web.Server(host = config.APP_HOST, port = config.APP_PORT, database = self.db, handler = handler)

		signal.signal(signal.SIGINT, self.handleSignal)
		signal.signal(signal.SIGTERM, self.handleSignal)

		signal.signal(signal.SIGINT, self.handleSignal)
		signal.signal(signal.SIGTERM, self.handleSignal)

		self.serverThread = threading.Thread(
			target = self.server.start,
			kwargs = {
				"startTasks": [
					lambda: controllers.user.loadSessions(self.db)
					]
				}
			)

		self.serverThread.start()

		while True:
			time.sleep(0.001) # cannot just pass because then CPU usage ramps to 30%
			# instead, the small wait allows some time between processes

	def shutdown(self):
		'''Shuts down the application'''
		if self.devServer:
			self.devServer.shutdown()
			self.devServer = None

		if self.db:
			self.db.close()
			self.db = None

		if self.server and self.server.running:
			if self.serverThread:
				context = zmq.Context()
				socket = context.socket(zmq.REQ)
				socket.connect("tcp://{host}:{port}".format(host = config.HOST, port = config.APP_PORT))
				socket.send("SOCKET_END")
				socket.close()
				self.serverThread.join()
				self.serverThread = None # make sure next serverThread.join does not run
			else:
				self.server.shutdown()

		self.server = None

		if self.serverThread:
			self.serverThread.join()

	def handleSignal(self, signal, frame):
		'''Handles an incoming signal'''
		sigNames = {
			2: "SIGINT",
			15: "SIGTERM"
			}
		print("Application: received {signal}; shutting down all".format(signal = sigNames.get(signal, signal)))
		self.shutdown()
		sys.exit(signal)

if __name__ == '__main__':
	app = start()
