# Rushy Panchal
# ai/tests/core/test_web.py

import unittest
import baseTests

import threading
import zmq

from core.web import Server

class TestServer(baseTests.BaseTest, unittest.TestCase):
	'''Tests the core.web.Server class'''
	base = Server

	@classmethod
	def setUpClass(cls):
		'''Set up the class'''
		def handler(db, data):
			'''Mock data handler'''
			return data
		cls.handler = handler
		cls.server = cls.base(host = "127.0.0.1", port = 7337, handler = handler)
		cls.socket = None

	@classmethod
	def tearDownClass(cls):
		'''Tear down the class'''
		if cls.socket:
			cls.socket.send("SOCKET_END")

	def test_hasStart(self):
		'''Server.start method exists'''
		self.assertHasAttr(self.base, "start")

	def test_hasShutdown(self):
		'''Server.shutdown method exists'''
		self.assertHasAttr(self.base, "shutdown")
