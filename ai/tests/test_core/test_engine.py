# Rushy Panchal
# ai/tests/core/test_engine.py

import unittest
import baseTests

from core.engine import Engine

class TestEngine(unittest.TestCase, baseTests.BaseTest, object):
	'''Tests the core.engine.Engine class'''
	def setUp(self):
		'''Sets up the test cases'''
		self.testClass = Engine

	def test_hasGetState(self):
		'''Engine.getState method exists'''
		self.assertFunctionExists(self.testClass, "getState")	

	def test_hasMakeMove(self):
		'''Engine.makeMove method exists'''
		self.assertFunctionExists(self.testClass, "makeMove")	
