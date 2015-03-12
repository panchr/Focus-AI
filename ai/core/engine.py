# Rushy Panchal
# ai/core/engine.py

from models.state import Gamestate

import shortid

class Engine(object):
	'''Basic Game Engine class'''
	random_id = shortid.ShortId()

	def __init__(self, rows = 8, columns = 8):
		self.games = {}
		self.numberGames = 0
		self.rows, self.columns = rows, columns

	def newGame(self, rows = None, columns = None):
		'''Adds a new game to the list of games'''
		gameID = self.random_id.generate()
		game = Gamestate.new(rows or self.rows, columns or self.columns)
		game[0: 2] = 1
		game[-2:] = 2
		self.games[gameID] = game
		self.numberGames += 1
		return gameID

	def getGame(self, gameID):
		'''Get the game by the game id'''
		return self.games[gameID]

	# old and new are tuples of (x, y) coordinates
	def makeMove(self, gameID, old, new):
		'''Move a piece to a new position'''
		return Gamestate.movePiece(self.games[gameID], old, new)
