# Rushy Panchal
# ai/core/database.py

import mongokit

from models.rule import Rule
from models.state import Gamestate

import config

class Database(mongokit.Connection):
	'''Specific database wrapper for a MongoDB database'''
	def getMatchingRules(self, state, stimuli):
		'''Finds the rules matching the patterns'''
		results = list(Rule.find({
			"condition": {"$in": stimuli},
			}).sort("weight", -1).limit(config.RULE_MATCHES))
		results.sort(key = lambda item: Gamestate.compare(state, item.state), reversed = True)
		return results
