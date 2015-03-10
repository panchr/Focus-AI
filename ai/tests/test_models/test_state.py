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
			np.zeros((2, 5), dtype = np.int32)
			)
			]
		self.stateA = np.zeros((8, 8), dtype = np.int32)
		self.stateB = np.zeros(self.stateA.shape, dtype = self.stateA.dtype)
		self.stateB[1] = 1 # difference of at least self.stateA.shape[0]
		self.stateB[2, 3] = 1
		self.stateA[1, 1] = 4
		# total difference is (5 + self.stateA.shape[0])
		self.stateC = np.zeros(self.stateA.shape, dtype = self.stateA.dtype)
		self.stateC[1, 1] = 1
		self.stateC[2, 2] = 1
		self.stateC[5, 4] = 1
		self.stateD = np.zeros(self.stateA.shape, dtype = self.stateA.dtype)
		self.stateD[1, 1] = 2
		self.stateD[6, 1] = 1
		self.stateE = np.zeros(self.stateA.shape, dtype = self.stateA.dtype)
		self.stateE[1, 1] = -2
		self.stateE[6, 3] = -1
		self.stateF = np.asarray([
			[0, 0, 0, 0, 0, 0, 0 ,0],
			[0, 0, 0, 0, 1, 0, 1 ,0],
			[0, 0, 1, -2, 0, 0, 1 ,0],
			[0, 0, 0, 0, 2, 1, 0 ,0],
			[0, 0, 1, 0, 2, 0, 0 ,0],
			[0, 0, 0, 2, 2, 0, 0 ,0],
			[0, 0, -1, 0, 0, 0, 0 ,0],
			[0, 0, 0, 0, 0, 0, 0 ,0],
			], dtype = np.int32)

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

	def test_isValid_simple(self):
		'''Gamestate.isValid (for simple moves) works'''
		self.assertTrue(self.model.isValid(self.stateB, (2, 3), (3, 4)))
		self.assertTrue(self.model.isValid(self.stateB, (1, 1), (2, 2)))
		self.assertTrue(self.model.isValid(self.stateB, (1, 5), (2, 6)))

		# These moves should fail - not valid board moves
		self.assertFalse(self.model.isValid(self.stateB, (1, 5), (2, 7)))
		self.assertFalse(self.model.isValid(self.stateB, (1, 0), (2, 7)))
		self.assertFalse(self.model.isValid(self.stateB, (1, 0), (1, 0)))

	def test_boardValidAndTaken_simple(self):
		'''Gamestate.boardValidAndTaken (for simple moves) works'''
		# no pieces should be taken for any simple move
		self.assertEquals(self.model.boardValidAndTaken(self.stateB, (2, 3), (3, 4)), (True, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateB, (1, 1), (2, 2)), (True, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateB, (1, 5), (2, 6)), (True, []))

		# These moves should fail - not valid board moves
		self.assertEquals(self.model.boardValidAndTaken(self.stateB, (1, 5), (2, 7)), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateB, (1, 0), (2, 7)), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateB, (1, 0), (1, 0)), (False, []))

	def test_isValid_taking(self):
		'''Gamestate.isValid (for taking moves) works'''
		self.assertTrue(self.model.isValid(self.stateF, (5, 3), [(3, 1), (1, 3)])) # double take
		self.assertTrue(self.model.isValid(self.stateF, (5, 3), [(3, 1)])) # single take is also valid
		self.assertTrue(self.model.isValid(self.stateF, (2, 3), [(0, 5), (2, 7)])) # King can take in all directions

		# Invalid board moves
		self.assertFalse(self.model.isValid(self.stateF, (5, 3), [(3, 1), (1, -1)])) # cannot move to a negative spot
		self.assertFalse(self.model.isValid(self.stateF, (5, 3), [(7, 1)])) # cannot go backwards because it's a regular piece
		self.assertFalse(self.model.isValid(self.stateF, (4, 4), [(2, 6)])) # must land on an empty spot
		self.assertFalse(self.model.isValid(self.stateF, (3, 4), [(1, 6)])) # must take a piece every step
		self.assertFalse(self.model.isValid(self.stateF, (3, 5), [(1, 7)])) # cannot take own piece
		self.assertFalse(self.model.isValid(self.stateF, (5, 3), [(3, 1), (2, 0)])) # must make consecutive jumps

	def test_boardValidAndTaken_taking(self):
		'''Gamestate.boardValidAndTaken (for taking moves) works'''
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (5, 3), [(3, 1), (1, 3)]), (True, [(4, 2), (2, 2)]))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (5, 3), [(3, 1)]), (True, [(4, 2)]))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (2, 3), [(0, 5), (2, 7)]), (True, [(1, 4), (1, 6)]))

		# Invalid board moves
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (5, 3), [(3, 1), (1, -1)]), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (5, 3), [(7, 1)]), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (4, 4), [(2, 6)]), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (3, 4), [(1, 6)]), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (3, 5), [(1, 7)]), (False, []))
		self.assertEquals(self.model.boardValidAndTaken(self.stateF, (5, 3), [(3, 1), (2, 0)]), (False, []))

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
			copyC[old] = 0
			copyC[new] = piece
			self.model.movePiece(self.stateC, old, new)
			self.assertTrue((self.stateC == copyC).all())

	def test_kingPromotion(self):
		'''Gamestate.movePiece promotes pieces to kings when necessary'''
		copyD = np.copy(self.stateD)

		copyD[1, 1] = 0
		copyD[0, 2] = -2
		self.model.movePiece(self.stateD, (1, 1), (0, 2))
		self.assertTrue((self.stateD == copyD).all())

		copyD[6, 1] = 0
		copyD[7, 0] = -1
		self.model.movePiece(self.stateD, (6, 1), (7, 0))
		self.assertTrue((self.stateD == copyD).all())

	def test_kingMove(self):
		'''Gamestate.movePiece correctly moves Kings'''
		copyE = np.copy(self.stateE)

		# try moving Player 2's King (-2) down
		copyE[1, 1] = 0
		copyE[2, 2] = -2
		self.model.movePiece(self.stateE, (1, 1), (2, 2))
		self.assertTrue((self.stateE == copyE).all())
		
		# move Player 2's King (-2) back up
		copyE[2, 2] = 0
		copyE[1, 3] = -2
		self.model.movePiece(self.stateE, (2, 2), (1, 3))
		self.assertTrue((self.stateE == copyE).all())

		# try moving Player 1's King (-1) down
		copyE[6, 3] = 0
		copyE[5, 2] = -1
		self.model.movePiece(self.stateE, (6, 3), (5, 2))
		self.assertTrue((self.stateE == copyE).all())
		
		# move Player 1's King (-1) back up
		copyE[5, 2] = 0
		copyE[6, 1] = -1
		self.model.movePiece(self.stateE, (5, 2), (6, 1))
		self.assertTrue((self.stateE == copyE).all())
