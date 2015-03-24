# Rushy Panchal
# ai/core/database.py

import mongokit

from models.rule import Rule
from models.state import Gamestate

import config

class Database(mongokit.Connection):
	'''Specific database wrapper for a MongoDB database'''
	def getStimuli(self):
		'''Get all of the stimuli from the database'''
		cursor = self.Rule.find({}, {"condition": 1})
		return map(lambda rule: rule.condition, list(cursor))

	def getMatchingRules(self, state, stimuli):
		'''Finds the rules matching the patterns'''
		results = list(self.Rule.find({
			"condition": {"$in": stimuli}, # might need to provide an encoded instance of Gamestate here
			}).sort("weight", -1).limit(config.RULE_MATCHES))
		results.sort(key = lambda item: Gamestate.compare(state, item.state), reverse = True)
		return results
