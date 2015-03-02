# Rushy Panchal
# ai/core/engine.py

from models.state import Gamestate

class Engine(object):
	'''Basic Game Engine class'''
	def __init__(self, rows = 8, columns = 8):
		self.rows = rows
		self.columns = columns
		self.state = Gamestate.new(rows, columns)

	# old and new are tuples of (x, y) coordinates
	def makeMove(self, old, new):
		'''Move a piece to a new position'''
		self.state.movePiece(old, new)
		if self.isValidState(state):
			return True
		return False
