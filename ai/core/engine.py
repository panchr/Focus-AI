# Rushy Panchal
# ai/core/engine.py

from models.state import Gamestate
from models.integer import Long

class Engine(object):
	'''Basic Game Engine class'''
	def __init__(self, rows = 8, columns = 8):
		self.rows = rows
		self.columns = columns
		self.state = Gamestate.new(rows, columns)

	def getState(self):
		'''Get the state of the current game'''
		return self.state

	# player is player number (player index + 1)
	# old and new are 0-indexed, 1-dimensional coordinates
	def makeMove(self, player, old, new):
		'''Move a piece to a new position'''
		gameState = self.getState()
		state = gameState[player]
		size = gameState[0]["size"] # the first element is metadata, including the size of the list
		# need to make sure that the spot is not already occupied already
		# also no point in moving if "old" is not a 1 currently
		state = Long(state).moveBit(old, new, size)
		if self.isValidState(state, player):
			self.state[player] = state
			return True
		return False

	def isValidState(state, position):
		'''Checks if the new state is valid'''
		individualStates = self.state[1:position] + state + self.state[position+1:]
		valid = 2**self.state[1]["size"] -1 # start off with all 1's
		for gameState in individualStates:
			valid &= gameState
		return (not valid) # state is valid if compound AND of all states is 0
