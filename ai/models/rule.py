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
		"weight": int, # might want to store it as a double instead so that all the weights can be normalized (instead of -infinity to +infinity, weights are 0 to 1)
		}
	
	required_fields = ["state", "weight", "condition", "response"]

	default_values = {
		"weight": 0
		}

	@staticmethod
	def new(state, condition, response):
		'''Creates a new rule'''
		rule = Model.connection.Rule()
		rule.state = state
		rule.condition = condition
		rule.response = response
		rule.save()
		return rule

	@Model.autosave
	def increaseWeight(self):
		'''Increments the weight'''
		self.weight += config.WEIGHT_DELTA
		if (self.weight + 1) >= config.NORMALIZE_THRESHOLD:
			Rule.normalize()

	@Model.autosave
	def decreaseWeight(self):
		'''Decreases the weight'''
		self.weight -= config.WEIGHT_DELTA
		if (self.weight - 1) <= config.NORMALIZE_THRESHOLD_NEG:
			Rule.normalize()

	@classmethod
	def normalize(cls):
		'''Normalizes all of the weights between 0 and 1'''
		raise NotImplementedError("Rule.normalize has not been implemented!")
		# weight = weight / (sum of all weights)
