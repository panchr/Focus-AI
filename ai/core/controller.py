# Rushy Panchal
# ai/core/controller.py

import config

class Controller(object):
	'''Main AI controller'''
	def __init__(self, db, engine):
		self.db = db
		self.engine = engine
		self.games = {}
		self.totalGames = 0

	def addGame(self):
		'''Adds a new game to the controller's list of games'''
		self.totalGames += 1
		self.games[self.totalGames] = []
		return self.totalGames

	def move(self, game):
		'''Make a move based on the current game state'''
		state = self.engine.getState()
		stimuli, responses = self.analyzeState(state)
		matchingRules = self.db.getMatchingRules(state, stimuli, responses)
		move = self.translateResponse(matchingRules[0])
		self.engine.makeMove(*move)

		self.games[game].append(move) # record move for this game

	def feedback(self, game, isHuman):
		'''Reports feedback for the game and modifies all of the rules if necessary'''
		for rule in self.games[game]:
			rule.increaseWeight(save = True) if isHuman else rule.decreaseWeight(save = True)

	def analyzeState(self, state):
		'''Analyzes the game state to get the current state and stimuli'''
		raise NotImplementedError("Controller.analyzeState not yet implemented")

	def translateResponse(self, response):
		'''Translates a response into a piece, old position, and new position'''
		raise NotImplementedError("Controller.translateResponse not yet implemented")
