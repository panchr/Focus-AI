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
		self.gameA = self.testObject.newGame()

	def test_hasNewGame(self):
		'''Engine.newGame method exists'''
		self.assertFunctionExists(self.testObject, "newGame")

	def test_hasMakeMove(self):
		'''Engine.makeMove method exists'''
		self.assertFunctionExists(self.testObject, "makeMove")	

	def test_hasGames(self):
		'''Engine.games exists'''
		self.assertHasAttr(self.testObject, "games")
		self.assertIsInstance(self.testObject.games, dict)

	def test_hasNumberGames(self):
		'''Engine.numberGames exists'''
		self.assertHasAttr(self.testObject, "numberGames")
		self.assertIsInstance(self.testObject.numberGames, int)

	def test_newGame(self):
		'''Engine.newGame works'''
		currentGames = self.testObject.numberGames
		gameID = self.testObject.newGame()
		self.assertIsInstance(gameID, basestring)
		self.assertEquals(self.testObject.numberGames, currentGames + 1)

	def test_makeMove(self):
		'''Engine.makeMove works'''
		pairs = [
			[(6, 5), (5, 4)],
			[(1, 1), (2, 2)],
			[(5, 4), (4, 5)]
			]
		copyState = np.copy(self.testObject.games[self.gameA])

		for old, new in pairs:
			piece = copyState[old]
			self.testObject.makeMove(self.gameA, old, new)
			copyState[old] = 0
			copyState[new] = piece
			self.assertTrue((self.testObject.games[self.gameA] == copyState).all())
