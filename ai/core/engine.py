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

	def endGame(self, gameID):
		'''Ends a current game'''
		del self.games[gameID]

	def getGame(self, gameID):
		'''Get the game by the game id'''
		return self.games[gameID]

	def setGame(self, gameID, newGame):
		'''Set the game to a new state'''
		self.games[gameID] = newGame

	def swapPlayer(self, gameID):
		'''Swap the current player to be moved'''
		currentPiece = self.gameMeta[gameID]["move"]
		newPiece = (1 if currentPiece == 2 else 2)
		self.gameMeta[gameID]["move"] = newPiece
		return newPiece

	# old and new are tuples of (x, y) coordinates
	def makeMove(self, gameID, old, new):
		'''Move a piece to a new position'''
		if (not gameID in self.games):
			return False, [], 0, False
		old, new = TO_TUPLE([old, new])
		game = self.games[gameID]
		gameMeta = self.gameMeta[gameID]
		playerToMove = game[old]
		if gameMeta["move"] == abs(playerToMove):
			boardValid, piecesTaken, upgraded = Gamestate.movePiece(game, old, new)
			if not boardValid:
				raise InvalidMove("Move is not valid")
			else:
				newPiece = self.swapPlayer(gameID)
				possibleWin = self.checkWin(gameID, newPiece)
				winner = abs(int(playerToMove if possibleWin else 0))
				# must explicitly convert to an int because otherwise it's an numpy.int64 (which can't be JSON serialized)
				# also need to only get the magnitude of it so that even if you win with a king, the piece type wins (and not the king itself)
				if winner:
					self.endGame(gameID)
				return boardValid, piecesTaken, winner, upgraded
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
