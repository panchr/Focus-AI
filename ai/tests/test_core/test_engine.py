# Rushy Panchal
# ai/tests/core/test_engine.py

import unittest
import baseTests
import numpy as np

from core.engine import Engine
from core.errors import WrongPlayerMove, InvalidMove

class TestEngine(baseTests.NumpyTest, unittest.TestCase):
	'''Tests the core.engine.Engine class'''
	testClass = Engine

	def setUp(self):
		'''Sets up the test cases'''
		self.testObject = self.testClass(8, 8)
		self.gameA = self.testObject.newGame()
		self.gameB = self.testObject.newGame()

	def test_hasNewGame(self):
		'''Engine.newGame method exists'''
		self.assertFunctionExists(self.testObject, "newGame")

	def test_hasMakeMove(self):
		'''Engine.makeMove method exists'''
		self.assertFunctionExists(self.testObject, "makeMove")	

	def test_hasReloadStimuli(self):
		'''Engine.reloadStimuli method exists'''
		self.assertFunctionExists(self.testObject, "reloadStimuli")

	def test_hasGetGame(self):
		'''Engine.getGame method exists'''
		self.assertFunctionExists(self.testObject, "getGame")

	def test_hasSetGame(self):
		'''Engine.setGame method exists'''
		self.assertFunctionExists(self.testObject, "setGame")

	def test_hasGames(self):
		'''Engine.games exists'''
		self.assertHasAttr(self.testObject, "games")
		self.assertIsInstance(self.testObject.games, dict)

	def test_hasGameMeta(self):
		'''Engine.gameMeta exists'''
		self.assertHasAttr(self.testObject, "gameMeta")
		self.assertIsInstance(self.testObject.gameMeta, dict)

	def test_hasGameStimuli(self):
		'''Engine.gameStimuli exists'''
		self.assertHasAttr(self.testObject, "gameStimuli")
		self.assertIsInstance(self.testObject.gameStimuli, list)

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
		self.assertEquals(len(self.testObject.games.keys()), currentGames + 1)
		self.assertEquals(len(self.testObject.gameMeta.keys()), currentGames + 1)

	def test_getGame(self):
		'''Engine.getGame works'''
		gameID = "abc"
		self.testObject.games[gameID] = 1
		self.assertEquals(self.testObject.games[gameID], self.testObject.getGame(gameID))

	def test_setgame(self):
		'''Engine.setGame works'''
		gameA = "gameA"
		gameB = "gameB"

		self.testObject.games[gameA] = "a"
		self.testObject.games[gameB] = "b"

		self.assertNotEquals(self.testObject.games[gameA], self.testObject.games[gameB])

		self.testObject.setGame(gameA, self.testObject.games[gameB])

		self.assertEquals(self.testObject.games[gameA], self.testObject.games[gameB])

	def test_makeMove(self):
		'''Engine.makeMove works'''
		pairs = [
			[(5, 4), (4, 5)],
			[(2, 1), (3, 0)],
			[(4, 5), (3, 6)]
			]
		copyState = np.copy(self.testObject.games[self.gameA])

		for old, new in pairs:
			piece = copyState[old]
			self.testObject.makeMove(self.gameA, old, new)
			copyState[old] = 0
			copyState[new] = piece
			self.assertTrue((self.testObject.games[self.gameA] == copyState).all())

	def test_makeMoveErrors(self):
		'''Engine.makeMove raises appropriate errors if necessary'''
		self.assertRaises(InvalidMove, self.testObject.makeMove, self.gameB, (-1, 0), (1, 1))
		self.assertRaises(WrongPlayerMove, self.testObject.makeMove, self.gameB, (0, 1), (1, 1))
		self.assertRaises(InvalidMove, self.testObject.makeMove, self.gameB, (7, 0), (3, 1))
