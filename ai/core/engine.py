# Rushy Panchal
# ai/core/engine.py

class Engine(object):
	'''Basic Game Engine class'''
	def getState(self):
		'''Get the state of the current game'''
		raise NotImplementedError("Engine.getState not yet implemented")

	def makeMove(self, piece, position, newPosition):
		'''Move a piece to a new position'''
		raise NotImplementedError("Engine.makeMove not yet implemented")
