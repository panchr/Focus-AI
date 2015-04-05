# Rushy Panchal
# ai/tests/core/test_engine.py

import unittest
import baseTests
import numpy as np

from core.engine import Engine
from core.errors import WrongPlayerMove, InvalidMove
import config

class TestEngine(baseTests.NumpyTest, unittest.TestCase):
	'''Tests the core.engine.Engine class'''
	testClass = Engine

	def setUp(self):
		'''Sets up the test cases'''
		self.testObject = self.testClass(8, 8)
		self.gameA = self.testObject.newGame()
		self.gameB = self.testObject.newGame()

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

	def test_checkWin(self):
		'''Engine.checkWin works'''
		game_id = "checkWin_id"
		state = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)
		self.testObject.games[game_id] = state

		self.assertEquals(self.testObject.checkWin(game_id), 0)

		state[state == 1] = 0
		self.assertEquals(self.testObject.checkWin(game_id), 2)
