# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase

import numpy as np
import math

import config

class Gamestate(CustomTypeBase):
	'''Depicts the game state'''
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

	@staticmethod
	def movePiece(state, old, new):
		'''Moves a piece in the game'''
		current = state[old]
		state[old] = state[new] # assumes that "new" is currently 0
		state[new] = current
		return True

	@staticmethod
	def isValid(state):
		'''Board is valid'''
		raise NotImplementedError("Gamestate.isValid has not been implemented yet")

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states'''
		raise NotImplementedError("Gamestate.compare has not been implemented yet")
