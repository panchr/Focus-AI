# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase
from models.integer import Integer, Long

class Gamestate(CustomTypeBase):
	'''Depicts the game state

	Each element of the list represents a player's bitstring.

	For example, Player 0 may have a bitstring of 0b10100000, or 160'''

	mongo_type = [int]
	python_type = [int]
	init_type = list

	@classmethod
	def new(cls, height = 8):
		'''Creates a new Game state descriptor'''
		return [[0] * height]

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states'''
		combinedA, combinedB = Long(0), Long(0)
		for valueA, valueB in zip(stateA, stateB):
			combinedA = combinedA.concat(valueA)
			combinedB = combinedB.concat(valueB)

		return abs(combinedA - combinedB)
