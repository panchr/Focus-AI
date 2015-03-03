# Rushy Panchal
# ai/tests/core/test_engine.py

import unittest
import baseTests
import numpy as np

from core.engine import Engine

class TestEngine(unittest.TestCase, baseTests.BaseTest, object):
	'''Tests the core.engine.Engine class'''
	def setUp(self):
		'''Sets up the test cases'''
		self.testClass = Engine
		self.testObject = self.testClass(8, 8)
		self.testObject.state[1, 1] = 1
		self.testObject.state[2, 2] = 1
		self.testObject.state[5, 4] = 1

	def test_hasMakeMove(self):
		'''Engine.makeMove method exists'''
		self.assertFunctionExists(self.testClass, "makeMove")	

	def test_makeMove(self):
		'''Engine.makeMove works'''
		pairs = [
			[(1, 1), (2, 3)],
			[(2, 2), (3, 4)],
			[(5, 4), (0, 0)]
			]
		copyState = np.copy(self.testObject.state)
		for old, new in pairs:
			self.testObject.makeMove(old, new)
			copyState[old] = 0
			copyState[new] = 1
			self.assertTrue((self.testObject.state == copyState).all())

	# need to make sure makeMove works as well
