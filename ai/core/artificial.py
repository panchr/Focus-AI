# Rushy Panchal
# ai/core/artificial.py

from core.errors import InvalidMove, WrongPlayerMove
from models.state import Gamestate

import numpy as np
import random
import operator

import config

class BaseAI(object):
	'''Base for all AI'''
	ADJACENT = [(y, x) for y in xrange(-1, 2) for x in xrange(-1, 2) if (x != 0 or y != 0)] # pre-compute the adjacent values

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

	def getAdjacent(self, position):
		'''Get the surrounding indices of a given position'''
		maxY, maxX = self.state.shape
		possible = map(lambda item: tuple( # need to explicitly convert to a tuple to allow for Numpy accesses
			map(operator.add, item, position)
			), self.ADJACENT) 
		return filter(lambda item: 0 <= item[0] < maxY and 0 <= item[1] < maxX, possible)

	def getOpenings(self, position):
		'''Get all adjacent openings for a given position'''
		possibilities = position if isinstance(position, list) else self.getAdjacent(position)
		# if adjacent positions are already provided, no need to recompute

		return filter(lambda possibility: self.state[possibility] == 0, possibilities)

	def getOpponentOccupied(self, position):
		'''Get all the adjacent occupied (by the opponent) for a given position'''
		possibilities = position if isinstance(position, list) else self.getAdjacent(position)
		# if adjacent positions are already provided, no need to recompute

		return filter(lambda possibility: self.state[possibility] != 0 and  self.state[possibility] != self.piece, possibilities)

class StaticAI(BaseAI):
	'''Represents a Static AI'''
	def makeMove(self):
		'''Make the AI's move'''
		takingFound = False
		openings, occupied = [], []
		positions = Gamestate.findLocations(self.state, self.piece)

		for position in positions:
			position_adjacent = self.getAdjacent(position)
			position_occupied = self.getOpponentOccupied(position_adjacent)

			# This implements a basic heuristic: if we have already found a taking move, no need to search for any simple moves (taking moves are always better)
			if (position_occupied or takingFound):
				occupied.extend(map(lambda newPosition: [position, newPosition],position_occupied))
				takingFound = True
			else:
				position_openings = self.getOpenings(position_adjacent)
				openings.extend(map(lambda newPosition: [position, newPosition],position_openings))

		# need to pick a random move from this
		# it would be best to evaluate the "score" of the given position to find the best option
		# then choose a random move out of the top 3 or so of these positions

		moveSuccess, playedMove = False, None

		random.shuffle(openings) # make sure we choose a random one each item
		for move in openings:
			try:
				moveSuccess = self.engine.makeMove(self.gameID, move)
				self.db.newRule(self.state, None, move, piece = self.piece) # need to find an actual stimulus - perhaps the pieces involved?
				playedMove = move
				break
			except InvalidMove:
				continue
			except WrongPlayerMove:
				break

		return moveSuccess, playedMove

class DynamicScriptingAI(StaticAI, BaseAI):
	'''Represents a Dynamic Scripting AI'''
	delta = config.WEIGHT_DELTA

	def makeMove(self):
		'''Makes the AI's move'''
		stimuli = self.analyzeStimuli()
		possibleMoves = self.db.getMatchingRules(self.state, stimuli, self.piece)

		if not possibleMoves:
			return self.bestNewMove()
			
		moveSuccess, playedMove = False, None

		for move in possibleMoves:
			try:
				moveSuccess = self.engine.makeMove(self.gameID, *move.response)
				playedMove = move
				break
			except InvalidMove:
				continue
			except WrongPlayerMove:
				break
		
		return moveSuccess, playedMove

	def analyzeStimuli(self):
		'''Analyzes the stimuli from the game and returns a list of potential stimuli'''
		return filter(lambda stimulus: ((self.state & stimulus) == stimulus).all(), self.possibleStimuli)

	def bestNewMove(self):
		'''Makes a randomized move that is weakly evaluated --- only should be executed if no valid moves exist in the database'''
		return super(DynamicScriptingAI, self).makeMove()
