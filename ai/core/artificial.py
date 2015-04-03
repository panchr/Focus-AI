# Rushy Panchal
# ai/core/artificial.py

from core.errors import InvalidMove, WrongPlayerMove

import numpy as np
import random

import config

class BaseAI(object):
	'''Base for all AI'''
	def __init__(self, database = None, engine = None, game = "", piece = 0):
		'''Initialize the AI'''
		self.db = database
		self.engine = engine
		self.gameID = game
		self.state = self.engine.getGame(self.gameID) if self.engine else ""
		self.possibleStimuli = self.engine.gameStimuli if self.db else []
		self.piece = piece

	def setState(self, newState):
		'''Sets the game state'''
		self.state = newState
		if self.engine:
			self.engine.setGame(self.gameID, newState)

	def makeMove(self):
		'''Should be overridden in the child class'''
		raise NotImplementedError("{cls}.makeMove not implemented".format(cls = self.__class__.__name__))

class StaticAI(BaseAI):
	'''Represents a Static AI'''
	def makeMove(self):
		'''Make the AI's move'''
		positions = zip(*np.where(self.state == self.piece))
		openings = []
		for position in positions:
			openings.extend(self.getOpenings(position))

	def getOpenings(self, position):
		'''Get all openings for a given position'''
		possibilities = [(0, 0)] * 9 # allocate all memory required beforehand
		index = 0
		for deltaX in xrange(-1, 2):
			for deltaY in xrange(-1, 2):
				possibilities[index] = (position[0] + deltaY, position[1] + deltaX)
				index += 1
		confirmedOpen = filter(lambda possibility: self.state[possibility] == 0, possibilities)
		return confirmedOpen

class DynamicScriptingAI(StaticAI, BaseAI):
	'''Represents a Dynamic Scripting AI'''
	delta = config.WEIGHT_DELTA

	def makeMove(self):
		'''Makes the AI's move'''
		stimuli = self.analyzeStimuli()
		possibleMoves = self.db.getMatchingRules(self.state, stimuli, self.piece)

		if not possibleMoves:
			return self.bestNewMove()
			
		moveSuccess = False

		for move in possibleMoves:
			try:
				moveSuccess = self.engine.makeMove(self.gameID, *move.response)
				break
			except InvalidMove:
				continue
			except WrongPlayerMove:
				break
		
		return moveSuccess, move

	def analyzeStimuli(self):
		'''Analyzes the stimuli from the game and returns a list of potential stimuli'''
		return filter(lambda stimulus: ((self.state & stimulus) == stimulus).all(), self.possibleStimuli)

	def bestNewMove(self):
		'''Makes a randomized move that is weakly evaluated --- only should be executed if no valid moves exist in the database'''
		return super(DynamicScriptingAI, self).makeMove()
