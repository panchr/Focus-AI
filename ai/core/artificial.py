# Rushy Panchal
# ai/core/artificial.py

import config

class DynamicScriptingAI(object):
	'''Represents a Dynamic Scripting AI'''
	delta = config.WEIGHT_DELTA

	def __init__(self, database = None, engine = None, game = ""):
		self.db = database
		self.engine = engine
		self.gameID = game
		self.game = self.engine.getGame(self.gameID)
		self.possibleStimuli = self.db.gameStimuli

	def makeMove(self):
		'''Makes the AI's move'''
		stimuli = self.analyzeStimuli()
		possibleMoves = self.db.getMatchingRules(self.game, stimuli)
		moveSuccess = False

		for move in possibleMoves:
			moveSuccess = self.engine.makeMove(self.gameID, *move.response)
			if moveSuccess:
				break
		
		return moveSuccess

	def analyzeStimuli(self):
		'''Analyzes the stimuli from the game and returns a list of potential stimuli'''
		return filter(lambda stimulus: ((self.state & stimulus) == stimulus).all(), self.stimuli)
		# could use ((state & stimuli) == stimuli).all()
		# this requires a list of stimuli, which means repeated database accesses
		# however, the stimuli aren't changing so this isn't an issue
		# raise NotImplementedError("DynamicScriptingAI.analyzeStimuli not yet implemented")
