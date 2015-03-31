# Rushy Panchal
# app/core/web.py

import zmq

class Server(object):
	'''A basic web server that handles connections'''
	def __init__(self, host = None, port = None, database = None, handler = None, recvSize = 1024):
		self.host = host or "127.0.0.1"
		self.port = port or 3000
		self.handler = handler
		self.db = database
		self.socketContext = zmq.Context()
		self.socket = self.socketContext.socket(zmq.REP)
		self.running = False

	def start(self, startTasks = []):
		'''Start the server'''
		self.running = True
		for task in startTasks:
			task()
		self.socket.bind("tcp://{host}:{port}".format(host = self.host, port = self.port))
		while self.running:
			message = self.socket.recv()
			if message == "SOCKET_END":
				print("ZMQ Server: received SOCKET_END; shutting down server")
				self.shutdown()
				break
			msg_id, response = self.handler(message)
			self.socket.send_json({
				"msg_id": msg_id,
				"response": response
				})

	def shutdown(self, endTasks = []):
		'''Shutdown the server'''
		print("ZMQ Server: shutting down server")
		self.running = False
		for task in endTasks:
			task()
		self.socket.close()
