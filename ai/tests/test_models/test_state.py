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
		self.mongoConversions = [
			([1, 2, 3], [1, 2, 3]),
			([4, 5, 6], [4, 5, 6]),
			([7, 8, 9], [7, 8, 9])
			]

	def test_compare(self):
		'''Test comparing two states'''
		stateA = [
			(8, 8, 64),
			0b0000000101000111110110000110111100000000001101000100111111001001,
			0b1100010010010000001001001000000000101001100010100010000000110110
			]
		stateB = [
			(8, 8, 64),
			0b0000000101000111110110000110111100000000001101000100111111001001,
			0b1100010010010000001001001000000000101001100010100010000001110110
			]
		self.assertEquals(self.model.compare(stateA, stateB), 64)
		self.assertEquals(self.model.compare(stateB, stateA), 64)
		self.assertEquals(self.model.compare(stateA, stateA), 0)
