# Rushy Panchal
# tests/models/test_state.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.state import Gamestate

class TestGamestate(unittest.TestCase, CustomTypeTestBase):
	'''Tests the models.state.Gamestate Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model = Gamestate
		self.modelObject = self.model()
		self.mongoConversions = [ # old mongo types
			([1, 2, 3], [1, 2, 3]),
			([4, 5, 6], [4, 5, 6]),
			([7, 8, 9], [7, 8, 9])
			]
