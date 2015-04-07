# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase

import numpy as np
import math

import config

class Gamestate(CustomTypeBase):
	'''Depicts the game state

	Each player is represented by an integer.
	A player's kings are represented by negative integers.'''
	mongo_type = list
	python_type = np.ndarray
	init_type = None

	def to_bson(self, value):
		'''Convert the structure to BSON'''
		return value.tolist()

	def to_python(self, value):
		'''Convert the structure to a Python list'''
		return np.asarray(value, dtype = config.STORAGE_DATATYPE)

	@classmethod
	def new(cls, width = 8, height = 8, dataType = config.STORAGE_DATATYPE, initialize = False):
		'''Creates a new Game state descriptor'''
		game = np.zeros((height, width), dtype = dataType)
		if initialize:
			cls.initialize(game)
		return game

	@classmethod
	def initialize(cls, game):
		'''Initializes the Gamestate'''
		rows = game.shape[0]
		midPoint = (rows + 1) / 2 - 1
		game[1:midPoint:2, 0::2] = 1
		game[:midPoint:2, 1::2] = 1
		game[rows - midPoint::2, 0::2] = 2
		game[rows - midPoint + 1::2, 1::2] = 2
		return game

	@classmethod
	def movePiece(cls, state, old, new):
		'''Moves a piece in the game'''
		try:
			simpleMove = isinstance(new[0], int)
			boardValid, piecesTaken = cls.boardValidAndTaken(state, old, new)
			if not boardValid:
				return False, []
		except IndexError:
			return False, []
		current = state[old]
		state[old] = 0
		for taken in piecesTaken: # won't run if it's a simple move because piecesTaken will be an empty list in that case
			state[taken] = 0
		newMove = new if simpleMove else new[-1]

		if ((current == 1 and newMove[0] == 7) or (current == 2 and newMove[0] == 0)):
			current *= -1 # piece reached the end of the board, so let's promote it to a King
		state[newMove] = current
		return True, piecesTaken

	@classmethod
	def boardValidAndTaken(cls, state, old, new):
		'''Determines if the board is valid and returns a list of taken pieces'''
		simpleMove = isinstance(new[0], int)
		toMove = state[old]
		deltaY = (new[0] if simpleMove else new[-1][0]) - old[0]
		deltaX = (new[1] if simpleMove else new[-1][1]) - old[1]
		absDeltaY = abs(deltaY)
		absDeltaX = abs(deltaX)

		conditions = [
			(old[0] >= 0), # cannot move to a negative side (which is jumping to the other side of the board)
			(old[1] >= 0),
			(toMove != 0),
			(deltaY > 0 if toMove == 1 else (deltaY < 0 if toMove == 2 else True)),
			# must be moving forward if Player 1, backwards if Player 2, or any direction if moving a King
			]
		takenPieces = []

		try:
			if simpleMove: # simple move
				conditions.extend([
					(new[0] >= 0),
					(new[1] >= 0),
					(state[new] == 0),
					(absDeltaY == 1), # can only be moving one piece
					(absDeltaX == 1)
					])
			else: # taking move
				currentPos = old
				for nextPos in new:
					takeDeltaY = nextPos[0] - currentPos[0]
					takeDeltaX = nextPos[1] - currentPos[1]
					inBetween = (currentPos[0] + takeDeltaY / 2, currentPos[1] + takeDeltaX / 2)

					takenPieces.append(inBetween)
					conditions.extend([
						(nextPos[0] >= 0), 
						(nextPos[1] >= 0),
						(state[nextPos] == 0), # spot must be empty
						(state[inBetween] != toMove), # cannot take own type of piece
						(state[inBetween] != 0), # middle spot cannot be empty, either
						(abs(takeDeltaX) == 2), # must be moving two spaces in either direction
						(abs(takeDeltaY) == 2),
						])

					currentPos = nextPos # advance a move

				conditions.extend([
					(absDeltaX % 2 == 0), # must move an even amount of spaces overall  
					(absDeltaY % 2 == 0),
					])
		except IndexError:
			return False, []
		boardValid = all(conditions)
		return boardValid, takenPieces if boardValid else []

	@classmethod
	def isValid(cls, state, old, new):
		'''New move is valid'''
		return cls.boardValidAndTaken(state, old, new)[0]

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states and returns the quotient of similarity'''
		difference = np.sum(abs(stateA ^ stateB))
		# max and min have to be converted to longs or we get an OverflowWarning because they are 32-bit integers (and multiplying them later on will take them over 32-bits)
		maxValue = long(max(np.max(stateA), np.max(stateB)))
		minValue = long(min(np.min(stateA), np.min(stateB)))
		arraySize = (stateA.size) * (maxValue - minValue)
		return float(arraySize - difference) / arraySize # doesn't account for position in the matrix, which is important

	@classmethod
	def findLocations(cls, state, piece):
		'''Find the locations of the piece on the board'''
		return zip(*np.where(state == piece))
