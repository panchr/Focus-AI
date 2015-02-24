# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase

class Gamestate(CustomTypeBase):
	'''Depicts the game state

	Each element of the list represents a player's bitstring.

	For example, Player 0 may have a bitstring of 0b10100000, or 160'''

	mongo_type = [int]
	python_type = [int]
	init_type = list # may have to change this to "list", because it should be callable

	@classmethod
	def new(cls, width = 8, height = 8):
		'''Creates a new Game state descriptor'''
		return [[0] * height for w in xrange(width)]
