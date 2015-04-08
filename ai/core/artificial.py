# Rushy Panchal
# ai/core/artificial.py

from core.errors import InvalidMove, WrongPlayerMove
from models.state import Gamestate
from models.game import Game

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
		self.opponentPiece = (1 if self.piece == 2 else 2)
		self.playedMoves = []
		self.history = []

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
		takingFound = False
		openings, attacks = [], []
		positions = Gamestate.findLocations(self.state, self.piece)

		for position in positions:
			position_attacks = Gamestate.getAttacks(self.state, position)

			# This implements a basic heuristic: if we have already found a taking move, no need to search for any simple moves (taking moves are always better)
			if (position_attacks or takingFound):
				attacks.extend(position_attacks)
				takingFound = True
			else:
				position_openings = Gamestate.getOpenings(self.state, position)
				openings.extend(map(lambda newPosition: [position, newPosition],position_openings))

		if attacks:
			attacks.sort(key = self.evaluateAttack)

			segmentOne, segmentTwo = attacks[:config.RULE_MATCHES], attacks[config.RULE_MATCHES:]
			# Shuffle the best and the worst segments separately, then re-combine them
			random.shuffle(segmentOne)
			random.shuffle(segmentTwo)

			moves = segmentOne + segmentTwo
		else:
			moves = position_openings
			random.shuffle(moves) # shuffle the moves to pick a random opening

		for move in moves:
			try:
				moveSuccess = self.engine.makeMove(self.gameID, *move)
				stimulus = self.generateStimulus(move)
				self.db.newRule(self.state, stimulus, move, piece = self.piece)
				playedMove = move
				break
			except InvalidMove:
				continue
			except WrongPlayerMove:
				break

		return moveSuccess, playedMove

	def evaluateAttack(self, attack):
		'''Evaluates the attack

		Currently, the evaluation simply consists of the number of pieces taken'''
		return len(attack[1])

	def generateStimulus(self, move):
		'''Generates a stimulus based on the move'''
		stimulus = Gamestate.new(initialize = False)

		start, end = move
		stimulus[start] = self.piece

		if isinstance(end, list): # "taking" move
			currentPiece = start
			for step in end:
				dY, dX = step[0] - currentPiece[0], step[1] - currentPiece[1]
				inBetween = (currentPiece[0] + dY / 2, currentPiece[1] + dX / 2)
				stimulus[inBetween] = self.opponentPiece # should take an opponent piece
				stimulus[step] = 3 # each step should be empty
				currentPiece = step
		else:
			stimulus[end] = 3 # for a simple move, the ending spot should be empty (3)

		return stimulus

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
				self.history.append(np.copy(self.state)) # it may be inefficient to keep so many copies of the game
				self.playedMoves.append(move)
				break
			except InvalidMove:
				continue
			except WrongPlayerMove:
				break
		
		return moveSuccess, playedMove.response

	def analyzeStimuli(self):
		'''Analyzes the stimuli from the game and returns a list of potential stimuli'''
		results = []
		for stimulus in self.possibleStimuli:
			emptyRequired = (self.state == 0) & (stimulus == 3) # select the spots that need to be empty and that are already empty
			opponentKings = (self.state == (-1 * self.opponentPiece))
			self.state[emptyRequired] = 3 # set those spots to empty
			self.state[opponentKings] *= -1 # change opponent kings to regular pieces

			if ((self.state & stimulus) == stimulus).all(): # check if the state matches the stimulus
				results.append(stimulus)

			self.state[emptyRequired] = 0 # reset for next step
			self.state[opponentKings] *= -1 # revert opponent kings
		return results

	def bestNewMove(self):
		'''Makes a randomized move that is weakly evaluated --- only should be executed if no valid moves exist in the database'''
		return super(DynamicScriptingAI, self).makeMove()

	def feedback(self, seemedHuman = False, details = ""):
		'''Provide feedback to the AI'''
		rules = map(lambda move: move._id, self.playedMoves)
		for rule in self.playedMoves:
			if seemedHuman:
				rule.increaseWeight()
			else:
				rule.decreaseWeight()
		return Game.new(feedback = details, history = self.history, rules = rules, seemedHuman = seemedHuman)
