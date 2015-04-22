# Rushy Panchal
# ai/core/engine.py

from models.state import Gamestate
from models.response import Response
from core.errors import WrongPlayerMove, InvalidMove

import shortid

TO_TUPLE = Response().to_python

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
		rows = rows or self.rows
		columns = columns or self.columns
		gameID = self.random_id.generate()
		game = Gamestate.new(rows, columns, initialize = True)

		self.games[gameID] = game
		self.gameMeta[gameID] = {
			"move": 2
			}
		self.numberGames += 1
		return gameID

	def getGame(self, gameID):
		'''Get the game by the game id'''
		return self.games[gameID]

	def setGame(self, gameID, newGame):
		'''Set the game to a new state'''
		self.games[gameID] = newGame

	# old and new are tuples of (x, y) coordinates
	def makeMove(self, gameID, old, new):
		'''Move a piece to a new position'''
		old, new = TO_TUPLE([old, new])
		game = self.games[gameID]
		gameMeta = self.gameMeta[gameID]
		playerToMove = game[old]
		if gameMeta["move"] == abs(playerToMove):
			boardValid, piecesTaken, upgraded = Gamestate.movePiece(game, old, new)
			if not boardValid:
				raise InvalidMove("Move is not valid")
			else:
				newPiece = (1 if playerToMove == 2 else 2)
				gameMeta["move"] = newPiece
				possibleWin = self.checkWin(gameID, newPiece)
				return boardValid, piecesTaken, (playerToMove if possibleWin else 0), upgraded
		else:
			raise WrongPlayerMove("Opposite Player Move or attempting to move a blank space")

	def checkWin(self, gameID, opponent):
		'''Check if a player has won the game'''
		state = self.games[gameID]
		positions = Gamestate.findLocations(state, opponent)
		for pos in positions: # if the list is empty (i.e no pieces left), then no iterations occur
			piece = state[pos]
			if Gamestate.getOpenings(state, pos) or Gamestate.getAttacks(state, pos): # there is an opening for an opponent move, either as a simple- or take- move
				return False
		return True
