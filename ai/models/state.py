# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase
from models.integer import Integer, Long

class Gamestate(CustomTypeBase):
	'''Depicts the game state

	Every element (other than the first) of the list represents a player's bitstring.
	The first element describes the width of each bitstring.

	For example, Player 0 may have a bitstring of 0b10100000, or 160'''

	mongo_type = [int]
	python_type = [int]
	init_type = list

	@classmethod
	def new(cls, width = 8, height = 8):
		'''Creates a new Game state descriptor'''
		return [{
			"width": width,
			"height": height,
			"size": width * height
			}]

	@staticmethod
	def compare(stateA, stateB):
		'''Compares two states'''
		difference = 0
		for valueA, valueB in zip(stateA[1:], stateB[1:]):
			difference += abs(valueA - valueB)
		return difference
