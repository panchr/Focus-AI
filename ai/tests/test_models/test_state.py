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
			("0,1,2|3,4,5|6,7,8", [
				[0, 1, 2],
				[3, 4, 5],
				[6, 7, 8]
				]),
			("11,12,13|21,22,23|31,32,33", [
				[11, 12, 13],
				[21, 22, 23],
				[31, 32, 33]
				]),
			("73,22,45|21|10,25,15,78|68,1,23,50,51", [
				[73, 22, 45],
				[21],
				[10, 25, 15, 78],
				[68, 1, 23, 50, 51]
				])
			]
