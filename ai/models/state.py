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
	def new(cls, width = 8, height = 8, dataType = config.STORAGE_DATATYPE):
		'''Creates a new Game state descriptor'''
		return np.zeros((width, height), dtype = dataType)

	@classmethod
	def movePiece(cls, state, old, new):
		'''Moves a piece in the game'''
		if not cls.isValid(state, old, new):
			return False
		current = state[old]
		state[old] = 0
		if not isinstance(new[0], int): # take-based move
			cls.takePieces(state, new)
		if ((current == 1 and new[0] == 7) or (current == 2 and new[0] == 0)):
			current *= -1 # piece reached the end of the board, so let's promote it to a King
		state[new] = current
		return True

	@classmethod
	def takePieces(cls, state, moves):
		'''Takes pieces between each move'''
		raise NotImplementedError("Gamestate.takePieces not yet implemented")

	@classmethod
	def isValid(cls, state, old, new):
		'''New move is valid'''
		simpleMove = isinstance(new[0], int)
		toMove = state[old]
		deltaY = (new[0] if simpleMove else new[-1][0]) - old[0]
		deltaX = (new[1] if simpleMove else new[-1][1]) - old[1]
		absDeltaY = abs(deltaY)
		absDeltaX = abs(deltaX)
		conditions = [
			(toMove != 0),
			(deltaY > 0 if toMove == 1 else (deltaY < 0 if toMove == 2 else True)),
			]
		if simpleMove: # simple move
			conditions.extend([
				(state[new] == 0),
				(absDeltaY == 1),
				(absDeltaX == 1)
				])
		else: # taking move
			numberMoves = len(new)
			if numberMoves == 1: # only taking one piece (might not need this - test soon)
				inBetween = (old[0] + deltaY / 2, old[1] + deltaX / 2)
				takeConditions = [
					(absDeltaX == 2),
					(absDeltaY == 2),
					(state[inBetween] == 1)
					]
			else:
				takeConditions = [] # preallocate the memory required - wait just kidding, too lazy for that
				currentPos = old
				for nextPos in new:
					takeDeltaY = nextPos[0] - currentPos[0]
					takeDeltaX = nextPos[1] - currentPos[1]
					inBetween = (currentPos[0] + takeDeltaY / 2, currentPos[1] + takeDeltaX / 2)

					takeConditions.extend([
						(state[nextPos] == 0),
						(state[inBetween] == 1),
						(takeDeltaX == 0 or abs(takeDeltaX) == 2),
						(abs(takeDeltaY) == 2),
						])

					currentPos = nextPos # advance a move
			#raise NotImplementedError("Gamestate.isValid -> take has not been implemented")
			conditions.extend([
				(absDeltaX % 2 == 0),
				(absDeltaY % 2 == 0),
				] + takeConditions)
		return all(conditions)

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states and returns the quotient of similarity'''
		difference = np.sum(abs(stateA ^ stateB))
		maxValue = max(np.max(stateA), np.max(stateB))
		minValue = min(np.min(stateA), np.min(stateB))
		arraySize = stateA.size * (maxValue - minValue)
		return float(arraySize - difference) / arraySize # doesn't account for position in the matrix, which is important
