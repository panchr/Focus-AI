# Rushy Panchal
# ai/models/rule.py

from models.model import Model
from models.state import Gamestate
from models.condition import Condition
from models.response import Response

import config

class Rule(Model):
	'''A general model for a Dynamic Scripting Rule'''
	__collection__ = "rulebase"

	structure = {
		"state": Gamestate(),
		"condition": Condition(),
		"response": Response(),
		"piece": int,
		"weight": float, # although weights are initially stored as integers, they are occasionally changed to floats so that they can be normalized
		}
	
	required_fields = ["state", "weight", "condition", "response", "piece"]

	default_values = {
		"weight": 0.0
		}

	@staticmethod
	def new(state, condition, response, piece = None, initialWeight = None):
		'''Creates a new rule'''
		rule = Model.connection.Rule()
		rule.state = state
		rule.condition = condition
		rule.response = response
		if initialWeight is not None:
			rule.weight = initialWeight
		if piece is None:
			piece = state[response[0]] if len(response) > 0 else 0
		rule.piece = piece
		rule.save()
		return rule

	@Model.autosave
	def increaseWeight(self):
		'''Increments the weight'''
		self.weight += config.WEIGHT_DELTA
		if (self.weight + 1) >= config.NORMALIZE_THRESHOLD:
			self.connection.Rule.normalize()

	@Model.autosave
	def decreaseWeight(self):
		'''Decreases the weight'''
		self.weight -= config.WEIGHT_DELTA
		if (self.weight - 1) <= config.NORMALIZE_THRESHOLD_NEG:
			self.connection.Rule.normalize()

	@classmethod
	def normalize(cls): # UNTESTED
		'''Normalizes all of the weights between 0 and 1'''
		rules = list(cls.connection.Rule.find())
		sumWeights = float(sum(map(lambda rule: rule.weight, rules)))
		for rule in rules:
			rule.weight = rule.weight / sumWeights
			rule.save()
