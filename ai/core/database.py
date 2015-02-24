# Rushy Panchal
# ai/core/database.py

import mongokit

from models.rule import Rule

import config

class Database(mongokit.Connection):
	'''Specific database wrapper for a MongoDB database'''
	def getMatchingRules(self, stimuli, responses):
		'''Finds the rules matching the patterns'''
		return list(Rule.find({
				"condition": {"$in": stimuli},
				"response": {"$in": responses}, 
				}).limit(config.RULE_MATCHES))
