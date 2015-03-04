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

	@staticmethod
	def isValid(state, old, new):
		'''New move is valid'''
		valid = (state[new] == 0) and (state[old] == 1)
		return valid

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states and returns the quotient of similarity'''
		difference = np.sum(abs(stateA ^ stateB))
		maxValue = max(np.max(stateA), np.max(stateB))
		minValue = min(np.min(stateA), np.min(stateB))
		arraySize = stateA.size * (maxValue - minValue)
		return float(arraySize - difference) / arraySize # doesn't account for position in the matrix, which is important
