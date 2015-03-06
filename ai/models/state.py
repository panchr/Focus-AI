# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase

import numpy as np
import math

import config

class Gamestate(CustomTypeBase):
	'''Depicts the game state

	Each player is represented by an integer.
	A player's kings are represented negative integers.'''
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
		state[old] = state[new]
		state[new] = current
		return True

	@classmethod
	def isValid(cls, state, old, new):
		'''New move is valid'''
		toMove = state[old]
		deltaY = new[0] - old[0]
		deltaX = new[1] - old[1]
		absDeltaY = abs(deltaY)
		absDeltaX = abs(deltaX)
		conditions = (
			(state[new] == 0),
			(toMove != 0),
			(deltaY > 0 if toMove == 1 else deltaY < 0),
			((absDeltaY == 1 and absDeltaX == 1) # normal move
				or ((absDeltaY % 2 == 0) and cls.isValidTake(state, old, new))), # moving over two pieces
			)
		return all(conditions)

	@classmethod
	def isValidTake(cls, state, old, new):
		'''Piece take is valid'''
		raise NotImplementedError("Gamestate.isValidTake not yet implemented")

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states and returns the quotient of similarity'''
		difference = np.sum(abs(stateA ^ stateB))
		maxValue = max(np.max(stateA), np.max(stateB))
		minValue = min(np.min(stateA), np.min(stateB))
		arraySize = stateA.size * (maxValue - minValue)
		return float(arraySize - difference) / arraySize # doesn't account for position in the matrix, which is important
