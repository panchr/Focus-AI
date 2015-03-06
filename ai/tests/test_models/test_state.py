# Rushy Panchal
# tests/models/test_state.py

import unittest
import baseTests
import numpy as np

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
		self.stateA = np.zeros((8, 8), dtype = np.uint32)
		self.stateB = np.zeros(self.stateA.shape, dtype = self.stateA.dtype)
		self.stateB[1] = 1 # difference of at least self.stateA.shape[0]
		self.stateB[2, 3] = 1
		self.stateA[1, 1] = 4
		# total difference is (5 + self.stateA.shape[0])
		self.stateC = np.zeros((8, 8), dtype = np.uint32)
		self.stateC[1, 1] = 1
		self.stateC[2, 2] = 1
		self.stateC[5, 4] = 1

	def test_toPython(self): # has to be custom because numpy array equality returns an array of booleans
		'''BSON to Python conversions'''
		for (bson, python) in self.mongoConversions:
			python_raw = self.modelObject.to_python(bson)
			self.assertTrue((python_raw == python).any())
			self.assertIsInstance(python_raw, type(python))

	def test_compareType(self):
		'''Gamestate.compare returns float'''
		self.assertIsInstance(self.model.compare(self.stateA, self.stateB), float)

	def test_compare(self):
		'''Gamestate.compare works'''
		maxValue = max(np.max(self.stateA), np.max(self.stateB))
		minValue = min(np.min(self.stateA), np.min(self.stateB))
		arraySize = self.stateA.size * (maxValue - minValue)
		expectedSimilarity = float(arraySize - self.stateA.shape[0] - 5) / arraySize
		givenSimilarity = self.model.compare(self.stateA, self.stateB)

		self.assertEquals(givenSimilarity, expectedSimilarity)
		self.assertEquals(self.model.compare(self.stateB, self.stateA), givenSimilarity)
		self.assertEquals(self.model.compare(self.stateA, self.stateA), 1)
		self.assertEquals(self.model.compare(self.stateB, self.stateB), 1)

	def test_isValid(self):
		'''Gamestate.isValid works'''
		self.assertTrue(self.model.isValid(self.stateB, (2, 3), (3, 4)))
		self.assertTrue(self.model.isValid(self.stateB, (1, 1), (2, 2)))
		self.assertTrue(self.model.isValid(self.stateB, (1, 5), (2, 6)))

		# These moves should fail - not valid board positions
		self.assertFalse(self.model.isValid(self.stateB, (1, 5), (2, 7)))
		self.assertFalse(self.model.isValid(self.stateB, (1, 0), (2, 7)))
		self.assertFalse(self.model.isValid(self.stateB, (1, 0), (1, 0)))

	def test_movePiece(self):
		'''Gamestate.movePiece works'''
		copyC = np.copy(self.stateC)
		pairs = [
			[(2, 2), (3, 3)],
			[(2, 3), (3, 4)],
			[(5, 4), (6, 3)]
			]

		for old, new in pairs:
			piece = copyC[old]
			self.model.movePiece(self.stateC, old, new)
			copyC[old] = 0
			copyC[new] = piece
			self.assertTrue((self.stateC == copyC).all())
