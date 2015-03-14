# Rushy Panchal
# ai/core/engine.py

from models.state import Gamestate
from core.errors import WrongPlayerMove, InvalidMove

import shortid

class Engine(object):
	'''Basic Game Engine class'''
	random_id = shortid.ShortId()

	def __init__(self, rows = 8, columns = 8, database = None):
		self.games = {}
		self.gameMeta = {}
		self.numberGames = 0
		self.rows, self.columns = rows, columns
		self.db = database
		self.gameStimuli = self.db.getStimuli() if self.db else []

	def reloadStimuli(self):
		'''Gets the stimuli from the database'''
		self.gameStimuli = self.db.getStimuli()

	def newGame(self, rows = None, columns = None):
		'''Adds a new game to the list of games'''
		gameID = self.random_id.generate()
		game = Gamestate.new(rows or self.rows, columns or self.columns)
		game[0: 2] = 1
		game[-2:] = 2
		self.games[gameID] = game
		self.gameMeta[gameID] = {
			"move": 2
			}
		self.numberGames += 1
		return gameID

	def getGame(self, gameID):
		'''Get the game by the game id'''
		return self.games[gameID]

	# old and new are tuples of (x, y) coordinates
	def makeMove(self, gameID, old, new):
		'''Move a piece to a new position'''
		game = self.games[gameID]
		gameMeta = self.gameMeta[gameID]
		playerToMove = game[old]
		if gameMeta["move"] == playerToMove:
			boardValid, piecesTaken = Gamestate.movePiece(game, old, new)
			if not boardValid:
				raise InvalidMove("Move was invalid")
			else:
				gameMeta["move"] = (1 if playerToMove == 2 else 2)
				return boardValid, piecesTaken
		else:
			raise WrongPlayerMove("Opposite Player Move")
