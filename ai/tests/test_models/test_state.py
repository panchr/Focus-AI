# Rushy Panchal
# tests/models/test_state.py

import unittest
import numpy as np
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
			([
				[1, 2, 1, 0],
				[0, 1, 2, 1]
				], 
			np.asarray([
				[1, 2, 1, 0],
				[0, 1, 2, 1]
				])
			),
			([
				[1, 1, 0, 0],
				[0, 0, 0, 1]
				], 
			np.asarray([
				[1, 1, 0, 0],
				[0, 0, 0, 1]
				])
			),
			([
				[0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0]
				],
			np.zeros((2, 5), dtype = np.uint32)
			)
			]

	def test_toPython(self): # has to be custom because numpy array equality returns an array of booleans
		'''BSON to Python conversions'''
		for (bson, python) in self.mongoConversions:
			python_raw = self.modelObject.to_python(bson)
			self.assertTrue((python_raw == python).any())
			self.assertIsInstance(python_raw, type(python))

	def test_compare(self):
		'''Test comparing two states'''
		# stateA = [
		# 	(8, 8, 64),
		# 	0b0000000101000111110110000110111100000000001101000100111111001001,
		# 	0b1100010010010000001001001000000000101001100010100010000000110110
		# 	]
		# stateB = [
		# 	(8, 8, 64),
		# 	0b0000000101000111110110000110111100000000001101000100111111001001,
		# 	0b1100010010010000001001001000000000101001100010100010000001110110
		# 	]
		# self.assertEquals(self.model.compare(stateA, stateB), 64)
		# self.assertEquals(self.model.compare(stateB, stateA), 64)
		# self.assertEquals(self.model.compare(stateA, stateA), 0)
		pass
